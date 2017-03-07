import os
import requests

class Gnip:
    """
    Thin wrapper around Gnip API
    """
    class GnipException(Exception):
        pass

    def __init__(self):
        self.gnip_username = os.environ.get('GNIP_USERNAME')
        self.gnip_password = os.environ.get('GNIP_PASSWORD')

        if not self.gnip_username:
            raise GnipException('No GNIP_USERNAME set in env')
        if not self.gnip_password:
            raise GnipException('No GNIP_PASSWORD set in env')

    def get_tweets_for_hashtag(self, hashtag, from_date=None, to_date=None, next_param=None):
        url = 'https://gnip-api.twitter.com/search/fullarchive/accounts/greg-students/prod.json'

        params = {
            'query': hashtag,
            'fromDate': from_date,
            'to_date': to_date,
            'next': next_param,
            'maxResults': 10
        }

        r = requests.get(
            url,
            auth=(self.gnip_username, self.gnip_password),
            params=params
        )

        return r.json()
