from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from partyparrots.settings import STATICFILES_DIRS
import json
import os

def get_leagues(request):
    ''' Reads the static/leagues.json file and 
        returns the contents of the file as a JSON object 
        Output structure = { "leagues" : [ 
			       { "league" : "...", 
                                 "logo": "...", 
                                 "clubs" : [
                                   { "name": "...", 
                                     "logo" : "..."
                                   }
                                 ,...] 
                               }
                              ,...]
                           }
    '''
    leagues_json_file = os.path.join(STATICFILES_DIRS[0], 'leagues.json')
    leagues_json = json.loads(open(leagues_json_file).read())
    return JsonResponse(leagues_json) 
