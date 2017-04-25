from pykafka import KafkaClient
from pykafka.common import OffsetType

from partyparrots.lib.twitter.twitter import StreamingTwitterData

import codecs

hashtags = [
    '#BVB',
    '#FCBayern',
    '#Atleti',
    '#FCBarcelona',
    '#realmadrid',
    '#SevillaFC',
    '#acmilan',
    '#ASRoma',
    '#inter',
    '#juventusfc',
    '#ChelseaFC',
    '#lfc',
    '#mcfc',
    '#mufc',
    '#thfc',
    '#PSG_inside',
    '#OL',
    '#AFC'
]

class TwitterKafkaProducer(StreamingTwitterData):

    def __init__(self, *args, **kwargs):
        self.client = KafkaClient(hosts='localhost:9092')
        self.topic = self.client.topics['realtime']
        self.producer = self.topic.get_producer()

        super(TwitterKafkaProducer, self).__init__(*args, **kwargs)

    def on_status(self, status):
        # print status.text
        tweet = codecs.encode(status.text, 'ascii', 'ignore')

        # self.producer.produce(status.text.decode('utf-8').encode('ascii', errors='ignore'))
        self.producer.produce(tweet)

if __name__ == '__main__':
    producer = TwitterKafkaProducer()
    producer.get_tweets_for_keywords(tracks=hashtags)
