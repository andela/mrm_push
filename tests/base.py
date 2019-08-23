import os
import sys

from flask_testing import TestCase
from alembic import command, config

from app import create_app
from api.v2.helpers.database import engine, db_session, Base
from api.v2.models.channels.channels_model import Channels

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

            channel = Channels(channel_id="calendar@id.com",
                               calendar_id="calendar@id.com-djfirnfn",
                               resource_id="9ty4bejkkw",
                               extra_atrributes='t284nff94nf', bouquet_id=1)
            channel.save()
            db_session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            command.stamp(self.alembic_configuration, 'base')
            db_session.remove()
            Base.metadata.drop_all(bind=engine)
