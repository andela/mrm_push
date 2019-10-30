import os
import sys

from flask_testing import TestCase
from alembic import command, config

from app import create_app
from api.v2.helpers.database import engine, db_session, Base
from api.v2.models.channels.channels_model import Channels
from api.v2.models.bouquets.bouquets_model import Bouquets

sys.path.append(os.getcwd())


class BaseTestCase(TestCase):
    alembic_configuration = config.Config("./alembic.ini")

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
            command.downgrade(self.alembic_configuration, '-1')
            command.upgrade(self.alembic_configuration, 'head')

            self.bouquet_200 = {
                "api_key1": "2123",
                "api_key2": "treat44",
                "auth_credentials": 'fdflfaw4',
                "bouquet_name": "Premium",
                "should_refresh": True,
                "refresh_url": 'http://localhost:5000/refresh'
            }

            self.bouquet_400_missing_key = {
                "api_key1": "2123",
                "api_key2": "treat44",
                "auth_credentials": 'fdflfaw4',
                "bouquet_name": "Premium",
                "should_refresh": True,
            }

            self.bouquet_400_null_string = {
                "api_key1": "2123",
                "api_key2": "treat44",
                "auth_credentials": 'fdflfaw4',
                "bouquet_name": "",
                "should_refresh": True,
                "refresh_url": 'http://localhost:5000/refresh'
            }

            self.bouquet_400_bn_numeral = {
                "api_key1": "2123",
                "api_key2": "treat44",
                "auth_credentials": 'fdflfaw4',
                "bouquet_name": 34,
                "should_refresh": True,
                "refresh_url": 'http://localhost:5000/refresh'
            }

            channel = Channels(channel_id="calendar@id.com",
                               calendar_id="calendar@id.com-djfirnfn",
                               resource_id="9ty4bejkkw",
                               extra_atrributes='t284nff94nf', bouquet_id=1)

            bouquet = Bouquets(api_key1="2123",
                               api_key2="treat44",
                               auth_credentials='fdflfaw4', bouquet_name="Premium",
                               should_refresh=True,
                               refresh_url='http://localhost:5000/refresh')

            channel.save()
            bouquet.save()

            db_session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            command.stamp(self.alembic_configuration, 'base')
            db_session.remove()
            Base.metadata.drop_all(bind=engine)
