import os
import sys
import datetime

from flask_testing import TestCase
from alembic import command, config

from app import create_app
from api.v2.helpers.database import engine, db_session, Base
from api.v2.models.channels.channels_model import Channels
from api.v2.models.bouquets.bouquets_model import Bouquets
from api.v2.models.subscriber.subscriber_model import Subscribers
from api.v2.models.subscription_method.subscription_method_model import Subscriptions
from api.v2.models.logs.logs_model import Logs

sys.path.append(os.getcwd())


class BaseTestCase(TestCase):
    alembic_configuration = config.Config('./alembic.ini')

    def create_app(self):
        app = create_app('testing')
        self.headers = {'content-type': 'application/json'}
        return app

    def setUp(self):
        app = self.create_app()
        self.app_test = app.test_client()
        with app.app_context():
            Base.metadata.create_all(bind=engine)

            command.stamp(self.alembic_configuration, 'head')
            command.upgrade(self.alembic_configuration, 'head')

            self.bouquet_201 = {
                'auth_uri': os.getenv('AUTH_URI'),
                'token_uri': os.getenv('TOKEN_URI'),
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'refresh_token': os.getenv('REFRESH_TOKEN'),
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob',
                                  'http://localhost'],
                'bouquet_name': 'Premium',
                'should_refresh': True,
                'refresh_url': 'https://regex101.com'
            }

            self.bouquet_201_return_data = {
                'data': {
                    'bouquet': {'auth_uri': 'https://h/o/oauth10/auth',
                                'bouquet_name': 'j', 'client_id': 'ug.apps',
                                'client_secret': 'X381OMrnCepN7DQ8LozG9orw',
                                'redirect_uris':
                                'urn:ietf:wg:oauth:2.0:oob http://localhost ',
                                'refresh_url': 'Nonek',
                                'should_refresh': False,
                                'token_uri': 'https://d.com/token'
                                }, 'message': 'successfully added bouquet'}}

            self.bouquet_400_missing_key = {
                'auth_uri': os.getenv('AUTH_URI'),
                'token_uri': os.getenv('TOKEN_URI'),
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'refresh_token': os.getenv('REFRESH_TOKEN'),
                'refresh_url': 'https://regex101.com',
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob',
                                  'http://localhost']
            }

            self.bouquet_400_null_string = {
                'auth_uri': os.getenv('AUTH_URI'),
                'token_uri': os.getenv('TOKEN_URI'),
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'refresh_token': os.getenv('REFRESH_TOKEN'),
                'refresh_url': 'https://regex101.com',
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob',
                                  'http://localhost'],
                'bouquet_name': ''
            }

            self.bouquet_400_bn_numeral = {
                'auth_uri': os.getenv('AUTH_URI'),
                'token_uri': os.getenv('TOKEN_URI'),
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'refresh_token': os.getenv('REFRESH_TOKEN'),
                'refresh_url': 'https://regex101.com',
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob',
                                  'http://localhost'],
                'bouquet_name': 78
            }

            self.bouquet_400_wrong_url = {
                'auth_uri': os.getenv('AUTH_URI'),
                'token_uri': os.getenv('TOKEN_URI'),
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'refresh_token': os.getenv('REFRESH_TOKEN'),
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob',
                                  'http://localhost'],
                'bouquet_name': 'Premium',
                'should_refresh': True,
                'refresh_url': 'https:m'
            }

            channel = Channels(
                    channel_id='1babe951eq0ru7d0e7r24fn2mm_R20191014T110000',
                    calendar_id='emile.nsengimana@andela.com',
                    resource_id='qwertyuioqwertyuioqwertyuioqwertyuio',
                    extra_atrributes='t284nff94nf', bouquet_id=1)

            log = Logs(calendar_id=1,
                       subscriber_name='request',
                       subscription_method='request',
                       payload='request',
                       timestamp=datetime.datetime.now())

            bouquet = Bouquets(
                auth_uri=os.getenv('AUTH_URI'),
                token_uri=os.getenv('TOKEN_URI'),
                client_id=os.getenv('CLIENT_ID'),
                client_secret=os.getenv('CLIENT_SECRET'),
                refresh_token=os.getenv('REFRESH_TOKEN'),
                redirect_uris='urn:ietf:wg:oauth:2.0:oob http://localhost',
                bouquet_name='Premium',
                should_refresh=True,
                refresh_url='http://localhost:5000/refresh'
            )

            bouquet_two = Bouquets(
                auth_uri=os.getenv('AUTH_URI'),
                token_uri=os.getenv('TOKEN_URI'),
                client_id='invalid token',
                client_secret=os.getenv('CLIENT_SECRET'),
                refresh_token=os.getenv('REFRESH_TOKEN'),
                redirect_uris='urn:ietf:wg:oauth:2.0:oob http://localhost',
                bouquet_name='Premium',
                should_refresh=True,
                refresh_url='http://localhost:5000/refresh'
            )

            channel = Channels(channel_id="564dfg67jn56h7jh6",
                               calendar_id="emilereas@gmail.com",
                               resource_id="9ty4bejkkfvdw",
                               extra_atrributes='t284nff94nf', bouquet_id=1)

            channel_two = Channels(channel_id="564dfg67jn56h7jh6n",
                               calendar_id="emilereasw@gmail.com",
                               resource_id="9ty4bejkkfvdww",
                               extra_atrributes='t284nff94nfn', bouquet_id=2)
            
            subscription = Subscriptions(name="compact")

            subscriber = Subscribers(subscriber_name="Manzi",
                               username="manzif6",
                               password="password1",
                               notification_url='https://notificati.com',
                               subscription_method_id=1,
                               bouquet_id=1)
            subscription.save()
            channel.save()
            channel_two.save()
            bouquet.save()
            bouquet_two.save()
            log.save()
            subscriber.save()

            db_session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            command.stamp(self.alembic_configuration, 'base')
            db_session.remove()
            Base.metadata.drop_all(bind=engine)
