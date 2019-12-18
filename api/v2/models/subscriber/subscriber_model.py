from sqlalchemy import (Column, String, Integer, Enum, ForeignKey, Text)
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import relationship

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType

from api.v2.models.subscription_method.subscription_method_model import Subscriptions


class Subscribers(Base, Utility):
    __tablename__ = 'subscribers'
    id = Column(Integer, Sequence('subscribers_id_seq', start=1, increment=1), primary_key=True)
    subscriber_name = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    notification_url = Column(Text, nullable=False)
    subscription_method_id = Column(Integer, ForeignKey('subscriptions.id',
                        name='fk_subscribers_subscriptions', ondelete='CASCADE'))
    bouquet_id = Column(Integer, ForeignKey('bouquets.id',
                        name='fk_subscribers_bouquets', ondelete='CASCADE'))
    subscription = relationship('Subscriptions', backref='subscriptions')

    def __init__(self, **kwargs):
        self.subscriber_name = kwargs['subscriber_name']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.notification_url = kwargs['notification_url']
        self.subscription_method_id = kwargs['subscription_method_id']
        self.bouquet_id = kwargs['bouquet_id']
