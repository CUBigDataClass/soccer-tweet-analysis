import argparse
import json
import os
import sys
import time
# from hdfs import InsecureClient

from partyparrots.lib.gnip.gnip import Gnip


if __name__ == '__main__':
    # set up the cmd line args - usage python gnip_hadoop.py '<your_hashtag>'
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'hashtag',
        help='Hashtag to search twitter'
    )

    args = parser.parse_args()
    print args.hashtag

    # client = InsecureClient('http://ec2-52-14-79-120.us-east-2.compute.amazonaws.com:50070', user='ubuntu')

    gnip = Gnip()

    next_param = None    

    while True:
        tweets = gnip.get_tweets_for_hashtag(
            hashtag=args.hashtag,
            next_param=next_param
        )

        current_time = time.strftime('%Y-%m-%d') + '_' + time.strftime('%H-%M-%S')

        if tweets['results']:
            with open(args.hashtag + '_' + current_time + '.txt', 'wb') as f:
                f.write(json.dumps(tweets))

        next_param = tweets['next']
        