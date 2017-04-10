from get_tweets import filtered_tweets

# Order the tweets by date and collect the tweet count for the said date
filtered_tweets.orderBy('date').groupBy('date').count().show()
