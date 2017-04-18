import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class DailyTweetCounts(DjangoCassandraModel):
    """
    Represents the daily tweet count of all the clubs
    """
    id=columns.UUID(primary_key=True, default=uuid.uuid4)
    club=columns.Text(required=True, index=True)
    date=columns.DateTime(required=True)
    count=columns.Integer(index=True)

class GeoTweets(DjangoCassandraModel):
    """
    Represents the geographic location of each tweet for all the clubs
    """
    id=columns.UUID(primary_key=True, default=uuid.uuid4)
    club=columns.Text(required=True)
    week_no=columns.Integer(required=True)
    count=columns.Integer(required=True)

class MonthlyTweetCounts(DjangoCassandraModel):
    """
    Represents the monthly tweet count of all the clubs
    """
    id=columns.UUID(primary_key=True, default=uuid.uuid4)
    month_no=columns.Integer(required=True)
    club=columns.Text(required=True)
    count=columns.Integer(required=True)

class GeoTweets(DjangoCassandraModel):
    """
    Represents the tweets filtered by based on whether they have geotags
    """
    id=columns.UUID(primary_key=True, default=uuid.uuid4)
    club=columns.Text(required=True, index=True)
    geo=columns.List(value_type=columns.Float(), required=True),
    text=columns.Text()
