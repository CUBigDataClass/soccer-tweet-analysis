from get_tweets import filtered_tweets
from pyspark.sql import SparkSession

if __name__ == "__main__":
    """if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)
    """
    
    spark = SparkSession.builder \
        .master("local") \
        .appName("Word Count") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    tweets_y = filtered_tweets.withColumn('year', year('date')).orderBy('year')
    tweets_ym = tweets_y.withColumn("month", month("date"))

    # Order tweets by year and then month with the count for each month
    tweets_ym.orderBy('year', 'month').groupBy('year','month').count().show()

    spark.stop()
