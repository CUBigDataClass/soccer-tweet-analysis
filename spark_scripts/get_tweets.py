from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode, col, udf
from pyspark.sql.types import DateType
from dateutil.parser import parse
from ConfigParser import SafeConfigParser

# get file path from hdfs config
config = SafeConfigParser()
config.read('../hdfs_config.ini')
host = config.get('main', 'host')
port = config.get('main', 'port')
dir_path = '/user/saurabh/#Atleti/*.txt'
file_path = host + port + dir _path

# Set the Spark context
conf = SparkConf().setMaster("local[*]").setAppName('pyspark')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# Convert the raw tweets into a dataframe
tweets = sqlContext.read.json(file_path)
tweets.registerTempTable('tweetTable')

# filter out the required attributes using explode and select
func = udf(lambda x: parse(x), DateType())
p = tweets.select(explode(tweets.results))
filtered_tweets = p.select('col.created_at', 'col.retweet_count', 'col.text', 'col.coordinates', 'col.user.verified', 'col.favorite_count')
filtered_tweets = filtered_tweets.withColumn('date', func(col('created_at')))
