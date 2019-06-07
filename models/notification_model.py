from helpers.database import Base
from utilities.utility import Utility
from sqlalchemy import (Column, String, Integer, Sequence)


class Notification(Base, Utility):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    results = Column(String)
    subscriber_info = Column(String)
    platform = Column(String)
