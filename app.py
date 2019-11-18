from flask import Flask, render_template, request, Response, jsonify
from flask_json import FlaskJSON
from flask_cors import CORS
from config import config
from service.push_notification import PushNotification
import os
import json


vapid_public_key = os.getenv("VAPID_PUBLIC_KEY")


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    FlaskJSON(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.route("/", methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route("/notifications", methods=['POST', 'GET'])
    def calendar_notifications():
        PushNotification().send_notifications_to_subscribers()
        result = PushNotification.send_notifications(PushNotification)
        return result


    @app.route("/channels", methods=['POST', 'GET'])
    def create_channels():
        return PushNotification.manual_create_channels(PushNotification)

    @app.route("/refresh", methods=['POST', 'GET'])
    def refresh():
        return PushNotification.manual_refresh(PushNotification)

    @app.route("/token", methods=['POST', 'GET'])
    def update_firebase_token():
        calendar_id = request.args.get('calendar_id')
        firebase_token = request.args.get('firebase_token')
        return PushNotification.update_firebase_token(PushNotification, calendar_id, firebase_token)

    @app.route("/get_notifications", methods=['GET'])
    def get_notifications():
        return PushNotification().get_notifications()

    @app.route("/subscription", methods=['POST', 'GET'])
    def subscribe():
        if request.method == "GET":
            return Response(response=json.dumps({"public_key": vapid_public_key}),
                            headers={"Access-Control-Allow-Origin": "*"},
                            content_type="application/json"
                            )
        subscription_info = request.get_json()["subscriber_info"]
        subscription = PushNotification().subscribe(subscription_info)
        return Response(status=201, response=json.dumps(subscription))

    @app.route("/googledb635995d37deb01.html", methods=['GET'])
    def verify_push_url():
        return render_template("googledb635995d37deb01.html")

    @app.route("/delete_room", methods=['DELETE'])
    def delete_room():
        calendar_id = request.args.get('calendar_id')
        return PushNotification().delete_room(calendar_id)

    @app.route("/add_room", methods=['GET', 'POST'])
    def add_room():
        calendar_id = request.args.get('calendar_id')
        firebase_token = request.args.get('firebase_token')
        return PushNotification().add_room(calendar_id, firebase_token)

    return app
