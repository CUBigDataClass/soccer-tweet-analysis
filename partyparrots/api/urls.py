from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'league/', get_league_data),
    url(r'geotweets/', get_geotagged_tweets),
    url(r'realtime', get_realtime_tweet),
]
