from sqlalchemy import (Column, String, Integer, Enum, ForeignKey, Text)
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import relationship

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType


class Subscriptions(Base, Utility):
    __tablename__ = 'subscriptions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
