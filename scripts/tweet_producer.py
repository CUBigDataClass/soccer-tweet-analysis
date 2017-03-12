import argparse
import json
import os
import sys

from pykafka import KafkaClient
from partyparrots.lib.gnip.gnip import Gnip


if __name__ == '__main__':
    # set up the cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', help='Kafka Topic to be used', required=True)
    parser.add_argument(
        '--hashtag',
        help='Hashtag to search twitter',
        required=True
    )

    args = parser.parse_args()

    # check for kafka hosts
    kafka_hosts = os.environ.get('KAFKA_HOSTS')
    if not kafka_hosts:
        print 'Kafka Hosts not configured'
        sys.exit(1)

    kafka_client = KafkaClient(
        hosts=kafka_hosts
    )

    topic = kafka_client.topics[args['--topic']]

    gnip = Gnip()

    next_param = None

    with topic.get_producer() as tweet_producer:
        while True:
            tweets = gnip.get_tweets_for_hashtag(
                hashtag=args['--hashtag'],
                next_param=next_param
            )

            if tweets['results']:
                for tweet in tweets['results']:
                    producer.produce(hashtag)

            next_param = tweets['next']
        
