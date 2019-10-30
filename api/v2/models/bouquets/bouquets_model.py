from sqlalchemy import (Column, String, Integer, Boolean, Enum)
from sqlalchemy.schema import Sequence

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType

class Bouquets(Base, Utility):
    __tablename__ = 'bouquets'
    id = Column(Integer, Sequence('bouquet_id_seq', start=1, increment=1), primary_key=True) # noqa
    bouquet_name = Column(String)
    refresh_url = Column(String, nullable=False)
    should_refresh = Column(Boolean, default=False)
    api_key1 = Column(String, nullable=False)
    api_key2 = Column(String, nullable=False)
    auth_credentials = Column(String, nullable=False)
    state = Column(Enum(StateType), nullable=False, default="active")

    def __init__(self, **kwargs):
        self.bouquet_name = kwargs['bouquet_name']
        self.refresh_url = kwargs['refresh_url']
        self.should_refresh = kwargs['should_refresh']
        self.api_key1 = kwargs['api_key1']
        self.api_key2 = kwargs['api_key2']
        self.auth_credentials = kwargs['auth_credentials']

    def refresh_channels(self):
        """Method for refreshing channels"""

        # TODO: add functionality to refresh and check channels using the refreshUrl

    def register_channels(self):
        """Method for registering channels"""

        # TODO: add functionality to add existing channels to a bouquet

    def receive_notification_from_google(self):
        """Method for receiving notification from google"""

        # TODO: add functionality to receive calendar notifications for purposes of logging them on the relay log table

    @staticmethod
    def add_bouquet(**kwargs):
        """Method for adding a bouquet"""
        x = Bouquets(**kwargs)
        x.save()
        # TODO: add functionality to add a bouquet on the bouquet table

    def delete_bouquet(self, bouquet_id):
        """Method for deleting a bouquet"""

        # TODO: add functionality to remove a listed bouquet from the bouquet table

    def add_calendar_to_bouquet(self, calendar_id, bouquet_id):
        """Method for adding a calendar to a bouquet"""

        # TODO: add functionality to add calendar to a bouquet upon subscription to receive notifications
