from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'league/', get_league_counts),
    url(r'geotweets/', get_geotagged_tweets),
    url(r'realtime', get_realtime_tweet),
    url(r'search/',get_search_tweets),
    url(r'fixtures/',get_club_fixtures),
    url(r'daily_tweet_counts/', get_daily_tweet_count)
]
