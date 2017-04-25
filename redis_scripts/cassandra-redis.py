from cassandra.cluster import Cluster
import redis

CASSANDRA_CLUSTER = '172.31.4.5'
CASSANDRA_CLUSTER_NAME = 'partyparrots'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

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

def write_to_redis():
    """
    Write tweets to redis
    """
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    geotweets_coordinates = get_geotweets_coordinates()
    geotweets_text = get_geotweets_with_text()
    for key in geotweets_coordinates:
        r.set('geotweets_coord_'+key, geotweets_coordinates[key])
    for key in geotweets_text:
        r.set('geotweets_text_'+key, geotweets_text[key])

if __name__ == '__main__':
    write_to_redis()

