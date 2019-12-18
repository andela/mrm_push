from api.v2.models.subscriber.subscriber_model import Subscribers as SubscriberModel
from api.v2.models.subscriber.subscriber_schema import SubscribersSchema

def get_subscribers(bouquet_id):
    subscribers = SubscriberModel.query.filter_by(bouquet_id=bouquet_id).all()
    if subscribers:
        return SubscribersSchema(many=True).dump(subscribers)

    return None

def get_subscriber(suscriber_id):
    subscriber = SubscriberModel.query.filter_by(id=suscriber_id).first()
    if subscriber:
        return SubscribersSchema(many=False).dump(subscriber)
    
    return None
