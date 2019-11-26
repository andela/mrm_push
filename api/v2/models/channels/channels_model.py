from sqlalchemy import (Column, String, Integer, Enum, ForeignKey)
from sqlalchemy.schema import Sequence

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType
from sqlalchemy.exc import IntegrityError
from api.v2.helpers.database import db_session


class Channels(Base, Utility):
    __tablename__ = 'channels'

    id = Column(Integer, Sequence('channels_id_seq', start=1, increment=1), primary_key=True) # noqa
    channel_id = Column(String, nullable=False)
    calendar_id = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    extra_atrributes = Column(String, nullable=False)
    bouquet_id = Column(Integer, ForeignKey('bouquets.id',
                        name='fk_channels_bouquets', ondelete='CASCADE'))
    state = Column(Enum(StateType), nullable=False, default="active")

    def __init__(self, **kwargs):
        self.channel_id = kwargs['channel_id']
        self.calendar_id = kwargs['calendar_id']
        self.resource_id = kwargs['resource_id']
        self.extra_atrributes = kwargs['extra_atrributes']
        self.bouquet_id = kwargs['bouquet_id']

    @staticmethod
    def save_channel(**kwargs):
        channel_saved = False
        try:
            register_channel = Channels(**kwargs)
            register_channel.save()
            channel_saved = True
        except IntegrityError:
            db_session.rollback()

        return channel_saved
