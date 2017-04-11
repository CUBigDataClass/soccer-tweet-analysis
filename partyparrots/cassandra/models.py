import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class DailyTweetCounts(DjangoCassandraModel):
    id=columns.UUID(primary_key=True, default=uuid.uuid4)
    club=columns.Text(required=True)
    date=columns.DateTime()
    count=columns.Integer(index=True)
