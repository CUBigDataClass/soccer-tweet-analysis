import os
import tweepy
from exceptions import TwitterDataException, TwitterException
from abc import ABCMeta, abstractmethod

class TwitterBase:
    """
    Abstract class representing a Twitter API object
    """

    __metaclass__ = ABCMeta

    _consumer_key = ""
    _consumer_secret = ""
    _access_token = ""
    _access_token_secret = ""
    api = None

    @abstractmethod
    def __init__(self):
        """
        Should set up the API Keys and OAuth tokens
        """
        consumer_key = os.environ.get('CONSUMER_KEY')
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

        if not consumer_key:
            raise TwitterException('CONSUMER_KEY')
        elif not consumer_secret:
            raise TwitterException('CONSUMER_SECRET')
        elif not access_token:
            raise TwitterException('ACCESS_TOKEN')
        elif not access_token_secret:
            raise(TwitterException('ACCESS_TOKEN_SECRET'))

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret

        # No Key related errors here
        # Let's (OAuth) Dance
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)

        # get the API object
        self.api = tweepy.API(auth)

class StreamingTwitterData(TwitterBase, tweepy.StreamListener):
    """
    Handler for Streaming Twitter Data
    """

    _tracks = None
    _filters = None
    _stream = None

    def __init__(self, tracks=None, filters=None):
        # initialize the base class constructor
        super(StreamingTwitterData, self).__init__()
        self.tracks = tracks
        self.filters = filters

        self._stream = tweepy.Stream(auth=self.api.auth, listener=self)

    def on_status(self, status):
        # got the status
        # TODO do something with the status
        print status.text

    def on_error(self, status_code):
        if status_code == 420:
            # Rate Limiting
            # TODO Do Backoff
            print 'Rate Limited'


    def get_tweets_for_keywords(self, tracks=None, filters=None):
        if not (tracks or self.tracks):
            raise TwitterDataException('No tracks specified')
        # some tracks specified

        applied_filters = None
        if filters:
            applied_filters = filters
        elif self._filters:
            applied_filters = self._filters

        if tracks:
            # currently specified tracks gets preference
            self._stream.filter(track=tracks, async=True)
        else:
            # we have previously specified tracks
            self._stream.filter(track=self._tracks, async=True)

class TimelineTwitterData(TwitterBase):
    """
    Used to access twitter feed of a particular handle
    """
    _handle = None

    def __init__(self, handle=None):
        # construct the base class
        super(TimelineTwitterData, self).__init__()

        self._handle = handle

    def get_tweets_for_handle(self, handle=None):
        if not (handle or self._handle):
            raise TwitterDataException('No Twitter handle specified')
        # we have a handle
        current_handle = self._handle
        if handle:
            current_handle = handle

        # use Cursor object to let Tweepy manage pagination
        statuses = []
        for status in tweepy.Cursor(self.api.user_timeline).pages():
            print status
            statuses.append(status)

        return statuses
