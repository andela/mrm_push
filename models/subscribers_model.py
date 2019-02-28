from helpers.database import Base
from utilities.utility import Utility
from models.calendar_model import Calendar
from sqlalchemy import (Column, String, Integer, Sequence, Boolean, Table, ForeignKey)
from sqlalchemy.orm import relationship

subscriber_calendars = Table("subscriber_calendars", Base.metadata,
                        Column('subscribers_id', Integer, ForeignKey('subscribers.id')),
                        Column('calendars_id', Integer, ForeignKey('calendars.id'))
                        )

class Subscriber(Base, Utility):
    __tablename__ = 'subscribers'
    id = Column(Integer, Sequence('subscribers_id_seq', start=1, increment=1),
                primary_key=True)
    platform = Column(String, nullable=False)
    subscription_info = Column(String, nullable=False)
    subscribed = Column(Boolean,nullable=False)
    calendars = relationship("Calendar", secondary=subscriber_calendars, backref="subscribers")
    subscriber_key = Column(String, nullable=False)
