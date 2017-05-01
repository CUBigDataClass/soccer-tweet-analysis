#!/usr/bin/python
import sys

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode, col, udf
from pyspark.sql.types import DateType
from dateutil.parser import parse
from ConfigParser import SafeConfigParser
from django.conf import settings

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partyparrots.settings")

import django
django.setup()

from partyparrots.cassandradata.models import DailyTweetCounts, GeoTweets


TEAM_HASHTAGS = {
    "#AFC": "Arsenal",
    "#ASRoma": "AS Roma",
    "#AllezParis": "PSG",
    "#Atleti": "Atletico Madrid",
    "#BVB": "Borussia Dortmund",
    "#CFC": "Chelsea",
    "#COYS": "Tottenham Hotspur",
    "#FCBarcelona": "FC Barcelona",
    "#FCBayern": "Bayern Munich",
    "#ForzaJuve": "Juventus",
    "#ForzaMilan": "AC Milan",
    "#HalaMadrid": "Real Madrid",
    "#Inter": "Internazionale",
    "#LFC": "Liverpool",
    "#MCFC": "Manchester City",
    "#MUFC": "Manchester United",
    "#OL": "Olympique Lyon",
    "#SevillaFC": "Sevilla",
}

# Set the Spark context
conf = SparkConf().setMaster("local[*]").setAppName('pyspark')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)


def get_filtered_tweets_for_hashtag(hashtag):

    print("Getting tweets for " + hashtag)

    dir_path = '/user/saurabh/' + hashtag + '/*.txt'
    file_path = "hdfs://ec2-13-58-118-205.us-east-2.compute.amazonaws.com:9000" + dir_path

    # Convert the raw tweets into a dataframe
    tweets = sqlContext.read.json(file_path)
    tweets.registerTempTable('tweetTable')

    # filter out the required attributes using explode and select
    func = udf(lambda x: parse(x), DateType())
    p = tweets.select(explode(tweets.results))
    filtered_tweets = p.select('col.created_at', 'col.retweet_count', 'col.text', 'col.coordinates', 'col.user.verified', 'col.favorite_count', 'col.geo')
    filtered_tweets = filtered_tweets.withColumn('date', func(col('created_at')))
    return filtered_tweets


def daily_counts(filtered_tweets):
    return filtered_tweets.orderBy('date').groupBy('date').count().collect()

def geo_tweet_filter(filtered_tweets):
    geo_tweets = filtered_tweets.filter(filtered_tweets.geo.isNotNull()).select('geo', 'text', 'date')
    return geo_tweets.select(geo_tweets.geo.coordinates, 'text', 'date').collect()

def _write_daily_counts_to_cassandra(club, filtered_tweets):
    daily_tweets = daily_counts(filtered_tweets)
    for row in daily_tweets:
        DailyTweetCounts.objects.create(
			count=row['count'],
            date=row.date,
			club=club
		)

def _write_geo_tweets_to_cassandra(club, filtered_tweets):
    geo_tweets = geo_tweet_filter(filtered_tweets)
    for row in geo_tweets:
        GeoTweets.objects.create(
            club=club,
            geo=row['geo.coordinates'],
            date=row.date,
            content=row.text
        )

# application start, loop through hashtags and write to cassandra
for (hashtag, club) in TEAM_HASHTAGS.iteritems():
    # get the filtered_tweets for the hashtag
    filtered_tweets = get_filtered_tweets_for_hashtag(hashtag)

    # write the daily counts to cassandra
    _write_daily_counts_to_cassandra(club, filtered_tweets)

    # write geo tweets to cassandra
    _write_geo_tweets_to_cassandra(club, filtered_tweets)
