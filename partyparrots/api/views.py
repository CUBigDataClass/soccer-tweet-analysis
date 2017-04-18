from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from collections import defaultdict

from partyparrots.api.methods import get_leagues
from partyparrots.cassandra.models import DailyTweetCounts

def get_league_data(request):
    leagues_json = get_leagues()

    results_dict = defaultdict(dict)

    for league in leagues_json:
        league_count = 0
        club_counts = {}
        for club in leagues_json[league]:
            # get counts for club
            query_results = DailyTweetCounts.objects.filter(
                club=club
            )
            league_count += query_results.count()
            club_count = 0

            for item in query_results:
                club_count += item.count
            club_counts[club] = club_count

        results_dict[league] = club_counts

    return JsonResponse(results_dict)
