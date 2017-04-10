from get_tweets import filtered_tweets
from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month

tweets_y = filtered_tweets.withColumn('year', year('date')).orderBy('year')
tweets_ym = tweets_y.withColumn("month", month("date"))

# Order tweets by year and then month with the count for each month
tweets_ym.orderBy('year', 'month').groupBy('year','month').count().show()
