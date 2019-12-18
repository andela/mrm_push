from ma import ma
from api.v2.models.subscription_method.subscription_method_model import Subscriptions


class SubscribersSchema(ma.Schema):
    class Meta:
        model = Subscriptions
        fields = ("id", "name")
