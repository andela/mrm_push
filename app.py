from flask import Flask, render_template
from flask_json import FlaskJSON
from config import config
from service.push_notification import PushNotification


def create_app(config_name):
    app = Flask(__name__)
    FlaskJSON(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.route("/", methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route("/notifications", methods=['POST', 'GET'])
    def calendar_notifications():
        return PushNotification.send_notifications(PushNotification)

    @app.route("/channels", methods=['POST', 'GET'])
    def create_channels():
        return PushNotification.create_channels(PushNotification)

    @app.route("/refresh", methods=['POST', 'GET'])
    def refresh():
        return PushNotification.refresh(PushNotification)

    return app
