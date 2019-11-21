from ma import ma
from api.v2.models.logs import logs_model as LogsModel

class LogsSchema(ma.Schema):
    class Meta:
        model = LogsModel
        fields = ('id', 'timestamp', 'calendar_id', 'subscriber_name', 'subscription_method', 'payload')

