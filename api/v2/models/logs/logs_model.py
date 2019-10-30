from sqlalchemy import (Column, String, Integer, Enum, DateTime, Text)
from sqlalchemy.schema import Sequence

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType

class Logs(Base, Utility):
    __tablename__ = 'logs'
    id = Column(Integer, Sequence('id', start = 1, increment = 1), primary_key = True)
    timestamp = Column(DateTime, nullable = False)
    calendar_id = Column(Text, nullable = False)
    subscriber_name = Column(Text, nullable = False)
    subscription_method = Column(Text, nullable = False)
    payload = Column(Text)

    def __init__ (self, **kwargs):
        self.timestamp = kwargs['timestamp']
        self.calendar_id = kwargs['calendar_id']
        self.subscriber_name = kwargs['subscriber_name']
        self.subscription_method = kwargs['subscription_method']
        self.payload = kwargs['payload']

    @staticmethod
    def save_log(**kwargs):
        register_log = Logs(**kwargs)
        register_log.save()

