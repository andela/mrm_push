from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS
from config import config

from api.v1 import api_v1
from api.v2 import api_v2


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    FlaskJSON(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)
    return app
