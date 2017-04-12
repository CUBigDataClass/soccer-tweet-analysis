#!/usr/bin/python
import sys

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode, col, udf, year, month, weekofyear
from pyspark.sql.types import DateType
from dateutil.parser import parse
from ConfigParser import SafeConfigParser

# get file path from hdfs config
config = SafeConfigParser()
config.read('../hdfs_scripts/hdfs_config.ini')
host = config.get('main', 'host')
port = config.get('main', 'port')

# Set the Spark context
conf = SparkConf().setMaster("local[*]").setAppName('pyspark')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def get_filtered_tweets_for_hashtag(hashtag):

    print("Getting tweets for " + hashtag)

    dir_path = '/user/saurabh/' + hashtag + '/*.txt'
    file_path = host + ':' + port + dir_path

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

def monthly_counts(filtered_tweets):
    tweets_y = filtered_tweets.withColumn('year', year('date')).orderBy('year')
    tweets_ym = tweets_y.withColumn("month", month("date"))
    return (tweets_ym, tweets_ym.orderBy('year', 'month').groupBy('year','month').count().show() )

def weekly_counts(tweets_ym):
    tweets_ymw = tweets_ym.withColumn('week', weekofyear('date'))
    return tweets_ymw.orderBy('year', 'month', 'week').groupBy('year','month', 'week').count().show()


# if __name__ == "__main__":
#
#     team_tag = sys.argv[1]
#
#     print("Getting tweets for " + team_tag)
#
#     # get file path from hdfs config
#     config = SafeConfigParser()
#     config.read('../hdfs_scripts/hdfs_config.ini')
#     host = config.get('main', 'host')
#     port = config.get('main', 'port')
#     dir_path = '/user/saurabh/' + team_tag + '/*.txt'
#     file_path = host + ':' + port + dir_path
#
#     print(file_path)
#
#     # Set the Spark context
#     conf = SparkConf().setMaster("local[*]").setAppName('pyspark')
#     sc = SparkContext(conf=conf)
#     sqlContext = SQLContext(sc)
#
#     # Convert the raw tweets into a dataframe
#     tweets = sqlContext.read.json(file_path)
#     tweets.registerTempTable('tweetTable')
#
#
#     # filter out the required attributes using explode and select
#     func = udf(lambda x: parse(x), DateType())
#     p = tweets.select(explode(tweets.results))
#     filtered_tweets = p.select('col.created_at', 'col.retweet_count', 'col.text', 'col.coordinates', 'col.user.verified', 'col.favorite_count', 'col.geo')
#     filtered_tweets = filtered_tweets.withColumn('date', func(col('created_at')))
#
#     print("getting geotweets for " + team_tag)
#     filtered_tweets.filter(filtered_tweets.geo.isNotNull()).select('geo').show()
#
#     print("getting daily counts for " + team_tag)
#     filtered_tweets.orderBy('date').groupBy('date').count().show()
#
#     tweets_y = filtered_tweets.withColumn('year', year('date')).orderBy('year')
#     tweets_ym = tweets_y.withColumn("month", month("date"))
#
#     # Order tweets by year and then month with the count for each month
#     print("getting monthly counts for " + team_tag)
#     tweets_ym.orderBy('year', 'month').groupBy('year','month').count().show()
#
#     tweets_ymw = tweets_ym.withColumn('week', weekofyear('date'))
#
#     # Order tweets by year, then month, then week with the count for each week
#     print("getting weekly counts for " + team_tag)
#     tweets_ymw.orderBy('year', 'month', 'week').groupBy('year','month', 'week').count().show()
