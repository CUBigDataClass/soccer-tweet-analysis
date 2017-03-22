from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from partyparrots.settings import STATICFILES_DIRS

import json
import os


def get_clubs(request):

    JSON_FILE_PATH = os.path.join(STATICFILES_DIRS[0], 'clubs.json')

    with open(JSON_FILE_PATH) as clubs_file:
        return JsonResponse(json.loads(clubs_file.read()))
