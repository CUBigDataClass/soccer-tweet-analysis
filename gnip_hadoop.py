import argparse
import json
import os
import sys
import time
import pydoop.hdfs as hdfs
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

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # client = InsecureClient('http://ec2-52-14-79-120.us-east-2.compute.amazonaws.com:50070', user='ubuntu')

    gnip = Gnip()

    next_param = None    

    while True:
        tweets = gnip.get_tweets_for_hashtag(
            hashtag=args.hashtag,
            next_param=next_param
        )

        current_time = time.strftime('%Y-%m-%d') + '_' + time.strftime('%H-%M-%S')
        file_dir = os.path.join(base_dir, args.hashtag)

        file_name = os.path.join(file_dir, args.hashtag + '_' + current_time + '.txt')

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


        if tweets['results']:
            with open(file_name, 'wb') as f:
                f.write(json.dumps(tweets))

            to_path = 'hdfs://localhost:9000/{hashtag}/{filename}'.format(hashtag=args.hashtag, filename=file_name)	    
            hdfs.put(file_name, to_path)

        next_param = tweets['next']
        
