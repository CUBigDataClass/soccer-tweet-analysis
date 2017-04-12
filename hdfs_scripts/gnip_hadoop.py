import argparse
import json
import os
import sys
import time
import pydoop.hdfs as hdfs
import tempfile
from ConfigParser import SafeConfigParser
from partyparrots.lib.gnip.gnip import Gnip


if __name__ == '__main__':
	# set up the cmd line args - usage python gnip_hadoop.py '<your_hashtag>'
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'hashtag',
		help='Hashtag to search twitter'
	)

	args = parser.parse_args()

	config = SafeConfigParser()
	config.read('hdfs_config.ini')

	host = config.get('main', 'host')
	port = int(config.get('main', 'port'))

	base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	hdfs_client = hdfs.hdfs(host=host, port=port)

	gnip = Gnip()

	next_param = None

	while True:
		tweets = gnip.get_tweets_for_hashtag(
			hashtag=args.hashtag,
			next_param=next_param,
			from_date=201501010000
		)

		file_dir = os.path.join(base_dir, args.hashtag) + '/'

		if not os.path.exists(file_dir):
			os.makedirs(file_dir)

		temp_file = tempfile.mkstemp(prefix=file_dir, suffix='.txt')

		hdfs_client.create_directory('{}'.format(args.hashtag))
		current_dir = hdfs_client.working_directory()

		if not os.path.exists(file_dir):
			os.makedirs(file_dir)

		if tweets.get('results', None):
			with open(temp_file[1], 'wb') as f:
				f.write(json.dumps(tweets))

			hdfs_path = current_dir + '/{hashtag}/{filename}'.format(hashtag=args.hashtag, filename=os.path.basename(temp_file[1]))
			hdfs.put(temp_file[1], hdfs_path)

		next_param = tweets['next']
