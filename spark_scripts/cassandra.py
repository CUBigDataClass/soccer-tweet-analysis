from django.conf import settings
from get_tweets import get_filtered_tweets_for_hashtag, daily_counts, monthly_counts, weekly_counts
from partyparrots.cassandra.models import DailyTweetCounts, WeeklyTweetCounts, MonthlyTweetCounts

TEAM_HASHTAGS = {
    "#AFC": "Arsenal",
    "#ASRoma": "AS Roma",
    "#AllezParis": "PSG",
    "#Atleti": "Atletico Madrid",
    "#BVB": "Borussia Dortmund",
    "#CFC": "Chelsea",
    "#COYS": "Tottenham Hotspur",
    "#FCBarcelona": "FC Barcelona",
    "#FCBayern": "Bayern Munich",
    "#ForzaJuve": "Juventus",
    "#ForzaMilan": "AC Milan",
    "#HalaMadrid": "Real Madrid",
    "#Inter": "Internazionale",
    "#LFC": "Liverpool",
    "#MCFC": "Manchester City",
    "#MUFC": "Manchester United",
    "#OL": "Olympique Lyon",
    "#SevillaFC": "Sevilla",
}


def _write_daily_counts_to_cassandra(club, filtered_tweets):
    for row in filtered_tweets:
        count = row.count
        date = row.date

        DailyTweetCounts.objects.create(
            club=club,
            count=count,
            date=date
        )


if __name__ == "__main__":
    for (hashtag, club) in TEAM_HASHTAGS:
        # get the filtered_tweets for the hashtag
        filtered_tweets = get_filtered_tweets_for_hashtag(hashtag)

        # write the daily counts to cassandra
        _write_daily_counts_to_cassandra(club, filtered_tweets)
        
