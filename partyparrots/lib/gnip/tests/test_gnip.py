import os
import mock
import unittest

from partyparrots.lib.gnip.gnip import Gnip

os.environ['GNIP_USERNAME'] = 'TEST_USERNAME'
os.environ['GNIP_PASSWORD'] = 'TEST_PASSWORD'

MOCK_TWITTER_RESPONSE = {
    'results': [
        {'text': 'Some New Text'},
        {'text': 'Some More New Text'}
    ],
    'requestParameters': {
        'fromDate': '201702050000',
        'maxResults': '10',
        'toDate': '201703070647'
    },
    'next': 'eyJhdXRoZW50aWNpdHkiOiJlNjZlZTBmZjlkN2FjMzM1NjQ1MmY0MjY4OTZiYjVjMzEwYzliOTY1ODljOGE2OTdhNThmNDVkMGEyODBjZWRkIiwiZnJvbURhdGUiOiIyMDE3MDIwNTAwMDAiLCJ0b0RhdGUiOiIyMDE3MDMwNzA2NDciLCJuZXh0IjoiMjAxNzAzMDcwNjQ2NDktODM5MDA0MzkzMDY0MjUxMzkyLTAifQ=='
}

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(MOCK_TWITTER_RESPONSE, 200)



class GnipTestCase(unittest.TestCase):
    def setUp(self):
        self.gnip = Gnip()

    @mock.patch('partyparrots.lib.gnip.gnip.requests.get', side_effect=mocked_requests_get)
    def test_hashtag_search(self, mock_get):
        query_response = self.gnip.get_tweets_for_hashtag(hashtag='afc')

        self.assertIsNotNone(query_response['results'])
        self.assertIsNotNone(query_response['requestParameters'])
        self.assertIsNotNone(query_response['next'])
        self.assertIsNotNone(len(query_response['results']), 2)
