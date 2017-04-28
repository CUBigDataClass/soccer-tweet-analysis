import redis
import ast
import os
import json
from elasticsearch import Elasticsearch

def get_geotagged_tweets(clubs):
    tweets = list()
    for club in clubs:
        r = redis.StrictRedis(host='localhost', port='6379', db=0)
        results = {'data': r.get('geotweets_text_'+club)}
        if results['data']:
            tweets.append(ast.literal_eval(results['data']))
    return tweets

def get_leagues():
    clubs = list()
    leagues_json_file = os.path.join('../partyparrots/static','leagues.json')

    with open(leagues_json_file) as json_file:
        f = json.load(json_file)
        for league in f:
            for club in f[league]:
                clubs.append(club)
    return get_geotagged_tweets(clubs)

def index_tweets():
    index_id = 1
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    all_club_data = get_leagues()

    for club in all_club_data:
        for tweet in club:
            es.create(index='geo_tweets', doc_type='football', id=index_id, body=tweet)
            index_id += 1

if __name__ == '__main__':
    index_tweets()