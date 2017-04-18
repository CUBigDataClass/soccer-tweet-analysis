import simplejson
import os
from partyparrots.settings import STATICFILES_DIRS

def get_leagues():
    leagues_json_file = os.path.join(STATICFILES_DIRS[0], 'leagues.json')

    with open(leagues_json_file) as json_file:
        return simplejson.load(json_file)
