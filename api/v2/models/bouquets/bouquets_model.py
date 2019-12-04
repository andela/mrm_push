from sqlalchemy import (Column, String, Enum, Sequence, Boolean, Integer)

from api.v2.helpers.database import Base
from api.v2.utilities.utility import Utility, StateType


class Bouquets(Base, Utility):
    __tablename__ = 'bouquets'
    id = Column(Integer, Sequence('bouquet_id_seq', start=1, increment=1), primary_key=True) # noqa
    bouquet_name = Column(String, nullable=True)
    refresh_url = Column(String, nullable=True, default="none")
    should_refresh = Column(Boolean, nullable=True, default=False)
    refresh_token = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    redirect_uris = Column(String, nullable=False)
    token_uri = Column(String, nullable=False)
    auth_uri = Column(String, nullable=False)
    state = Column(Enum(StateType), nullable=False, default="active")

    def __init__(self, **kwargs):
        self.bouquet_name = kwargs['bouquet_name']
        self.client_id = kwargs['client_id']
        self.client_secret = kwargs['client_secret']
        self.redirect_uris = kwargs['redirect_uris']
        self.auth_uri = kwargs['auth_uri']
        self.token_uri = kwargs['token_uri']
        self.refresh_token = kwargs['refresh_token']

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

        bouquet = Bouquets(**kwargs)
        bouquet.save()

        # TODO: add functionality to add a bouquet on the bouquet table

    def delete_bouquet(self, bouquet_id):
        """Method for deleting a bouquet"""

        # TODO: add functionality to remove a listed bouquet from the bouquet table

    def add_calendar_to_bouquet(self, calendar_id, bouquet_id):
        """Method for adding a calendar to a bouquet"""

        # TODO: add functionality to add calendar to a bouquet upon subscription to receive notifications
