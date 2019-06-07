from helpers.database import Base
from utilities.utility import Utility
from sqlalchemy import (Column, String, Integer, Sequence)


class Calendar(Base, Utility):
    __tablename__ = 'calendars'
    id = Column(Integer, Sequence('calendars_id_seq', start=1, increment=1),
                primary_key=True)
    calendar_id = Column(Integer, nullable=False)
    channel_id = Column(String, nullable=True)
    resource_id = Column(String, nullable=True)
    firebase_token = Column(String, nullable=True)
