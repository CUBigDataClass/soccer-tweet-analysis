from cassandra.cluster import Cluster
from collections import defaultdict
import redis
import json
import os

CASSANDRA_CLUSTER = '172.31.4.5'
CASSANDRA_CLUSTER_NAME = 'partyparrots'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
STATICFILES_DIR = '../partyparrots/static/'

def get_leagues():
    leagues_json_file = os.path.join(STATICFILES_DIR, 'leagues.json')

    with open(leagues_json_file) as json_file:
        return json.load(json_file)

def get_geotweets():
    """
    Fetch geotagged tweets from cassandra cluster
    """
    cluster = Cluster([CASSANDRA_CLUSTER])
    session = cluster.connect(CASSANDRA_CLUSTER_NAME)
    query_results = session.execute('select club, geo, text from geo_tweets')
    return query_results

def get_geotweets_coordinates():
    """
    Extract longitude, latitude from geotweets
    """
    query_results = get_geotweets()
    results = {}
    for item in query_results:
        tweet = {}
        club = item.club
        if club not in results:
            results[club] = []
        tweet["lat"] = item.geo[0]
        tweet["lon"] = item.geo[1]
        results[club].append(tweet)
    return results

def get_geotweets_with_text():
    """
    Extract longitude, latitude, text from geotweets
    """
    query_results = get_geotweets()
    results = {}
    for item in query_results:
        tweet = {}
        club = item.club
        if club not in results:
            results[club] = []
        tweet["text"] = item.text.encode('ascii', 'ignore').replace("'", "").replace("\"", "")
        tweet["lat"] = item.geo[0]
        tweet["lon"] = item.geo[1]
        results[club].append(tweet)
    return results

def get_league_data():
    """
    Get total count of tweets for each club from cassandra cluster
    """
    cluster = Cluster([CASSANDRA_CLUSTER])
    session = cluster.connect(CASSANDRA_CLUSTER_NAME)
    leagues = get_leagues()
    query_results = defaultdict(dict)
    for league in leagues:
        for club in leagues[league]:
            result = session.execute("select sum(count) as sum from daily_tweet_counts where club='{}'".format(club))[0]
            club_count = result.sum
            query_results[league][club] = club_count
    return query_results

def get_daily_counts():
    """
    Get daily tweet counts
    """
    cluster = Cluster([CASSANDRA_CLUSTER])
    session = cluster.connect(CASSANDRA_CLUSTER_NAME)
    leagues = get_leagues()
    query_results = {}
    for league in leagues:
        for club in leagues[league]:
            result = session.execute("select count, date from daily_tweet_counts where club='{}'".format(club))
            query_results[club] = result.current_rows
    return query_results


def write_to_redis():
    """
    Write tweets to redis
    """
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    geotweets_coordinates = get_geotweets_coordinates()
    geotweets_text = get_geotweets_with_text()
    leagues_count = get_league_data()
    daily_tweet_counts = get_daily_counts()
    for key in geotweets_coordinates:
        r.set('geotweets_coord_'+key, geotweets_coordinates[key])
    for key in geotweets_text:
        r.set('geotweets_text_'+key, geotweets_text[key])
    for key in daily_tweet_counts:
        r.set('daily_count_'+key, daily_tweet_counts[key])
    league_counts = {}
    for league in leagues_count:
        club_counts = {}
        for club in leagues_count[league]:
            club_counts[club] = leagues_count[league][club]
        league_counts[league] = club_counts
    league_counts = str(league_counts).replace("u\'", "\'")
    r.set('league_counts', league_counts)



if __name__ == '__main__':
    write_to_redis()
