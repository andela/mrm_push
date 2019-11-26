from __future__ import print_function

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from api.v2.models.bouquets.bouquets_model import Bouquets


def check_bouquet_credentials(data):
    """
    :param data:
    :return: service object and refresh_token
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Check if client_secret exists in the db
    _bouquet = Bouquets.query.filter_by(client_secret=data['client_secret']).first()
    if not _bouquet:
        client_config = {
            'installed': {
                'auth_uri': data['auth_uri'],
                'token_uri': data['token_uri'],
                'redirect_uris': data['redirect_uris'],
                'client_id': data['client_id'],
                'client_secret': data['client_secret']
            }
        }

        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        credentials = flow.run_local_server(port=0)

    else:
        credentials = Credentials(
            None,
            refresh_token=_bouquet.refresh_token,
            token_uri=_bouquet.token_uri,
            client_id=_bouquet.client_id,
            client_secret=_bouquet.client_secret
        )

    service = build('calendar', 'v3', credentials=credentials)
    return {'service': service, 'refresh_token': credentials.refresh_token}
