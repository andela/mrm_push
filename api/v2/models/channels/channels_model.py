from sqlalchemy import (Column, String, Integer, Enum)
from sqlalchemy.schema import Sequence

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType


class Channels(Base, Utility):
    __tablename__ = 'channels'
    id = Column(Integer, Sequence('channels_id_seq', start=1, increment=1), primary_key=True)  # noqa
    channel_id = Column(String, nullable=True)
    calendar_id = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    extra_atrributes = Column(String, nullable=True)
    bouquet_id = Column(Integer)
    state = Column(Enum(StateType), nullable=False, default="active")

    def __init__(self, **kwargs):
        self.channel_id = kwargs['channel_id']
        self.calendar_id = kwargs['calendar_id']
        self.resource_id = kwargs['resource_id']
        self.extra_atrributes = kwargs['extra_atrributes']
        self.bouquet_id = kwargs['bouquet_id']
