from cassandra.cluster import Cluster
import redis

def get_geotweets():
    """
    Fetch geotagged tweets from cassandra cluster
    """
    cluster = Cluster(['172.31.4.5'])
    session = cluster.connect('partyparrots')
    query = session.execute('select club, geo, text from geo_tweets')
    results = {}
    for item in query:
        club = item.club
        if club not in results:
            results[club] = []
        results[club].append([item.geo[0], item.geo[1], item.text])
    return results

def connect_to_redis():
    """
    Write tweets to redis
    """
    r = redis.StrictRedis(host='localhost', port='6379', db=0)
    geotweets = get_geotweets()
    r.set('geotweets', geotweets)

connect_to_redis()

