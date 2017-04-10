from tweet_dataframe import filtered_tweets


tweets_y = filtered_tweets.withColumn('year', year('date')).orderBy('year')
tweets_ym = tweets_y.withColumn("month", month("date"))
tweets_ymw = tweets_ym.withColumn('week', weekofyear('date'))

# Order tweets by year, then month, then week with the count for each week
tweets_ymw.orderBy('year', 'month', 'week').groupBy('year','month', 'week').count().show()
