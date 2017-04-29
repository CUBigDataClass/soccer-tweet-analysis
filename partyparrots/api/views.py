from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.db import connection
import json
from collections import defaultdict
from pykafka import KafkaClient

from partyparrots.api.methods import get_leagues
from partyparrots.settings import FIXTURES_DIR
from elasticsearch import Elasticsearch

import redis
import os

#KAFKA_CLIENT = KafkaClient(hosts="127.0.0.1:9092")

#TOPIC = KAFKA_CLIENT.topics['realtime']

#KAFKA_CONSUMER = TOPIC.get_simple_consumer(
#    consumer_group='partyparrots'
#)

def get_league_data(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        leagues_json = get_leagues()
        results_dict = defaultdict(dict)

        for league in leagues_json:
            league_count = 0
            for club in leagues_json[league]:
                result = cursor.execute("select sum(count) as sum from daily_tweet_counts where club='{}'".format(club))
                club_count = result[0]['sum']
                league_count += club_count
                results_dict[league][club] = club_count
        return JsonResponse(results_dict)
    else:
        request.set_status(405)

def get_league_counts(request):
    if request.method == 'GET':
        r = redis.StrictRedis(host='localhost', port='6379', db=0)
        results = r.get('league_counts').replace('\'', '"')
        return JsonResponse(json.loads(results))
    else:
        request.set_status(405)

def get_geotagged_tweets(request):
    r = redis.StrictRedis(host='localhost', port='6379', db=0)
    results = {'data': r.get('geotweets_text_'+'Liverpool')}
    return JsonResponse(results)

def get_search_tweets(request):
    es = Elasticsearch([{'host':'localhost', 'port':9200}])
    es.indices.put_settings(index="geo_tweets", body= {"index" : { "max_result_window" : 70000 }})

    query = request.GET.get("q")
    result = es.search(q=query,size=70000)
    return JsonResponse({
        "results": result['hits']['hits']
    })

def get_realtime_tweet(request):
    tweet = KAFKA_CONSUMER.consume()
    KAFKA_CONSUMER.commit_offsets()

    response = {
        'tweet': tweet.value
    }
    return JsonResponse(response)

def get_club_fixtures(request):
    clubs = {'Manchester United':'mufc',"Liverpool":'liverpool','Arsenal':'arsenal','Tottenham Hotspur':'spurs',
            'Manchester City':'mcfc','Chelsea':'chelsea','Real Madrid':'madrid','Atletico Madrid':'atletico',
            'Bayern Munich':'bayern','Borussia Dortmund':'dortmund','Inter Milan':'inter','AC Milan':'milan',
            'Juventus':'juventus','AS Roma':'roma','Paris Saint Germain':'psg','Lyon':'lyon','Sevilla':'sevilla',
            'Barcelona':'barcelona'}

    club = request.GET.get("club")
    fixtures = os.path.join(FIXTURES_DIR, clubs[club])
    with open(fixtures, 'rb') as f:
        res = {
            "club": json.loads(f.read())
        }
        return JsonResponse(res)
