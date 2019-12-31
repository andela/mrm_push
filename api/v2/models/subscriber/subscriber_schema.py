from ma import ma
from api.v2.models.subscriber.subscriber_model import Subscribers


class SubscribersSchema(ma.Schema):
    class Meta:
        model = Subscribers
        fields = ("id", "subscriber_name", "username",
                  "notification_url", "subscription_method_id", "bouquet_id", "subscription")
