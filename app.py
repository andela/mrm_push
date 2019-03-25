from flask import Flask, render_template, request, Response
from flask_json import FlaskJSON
from flask_cors import CORS
from config import config
from service.push_notification import PushNotification
from service.subscribers import Subscriber
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
        return PushNotification().send_notifications()

    @app.route("/get_notifications", methods=['GET'])
    def get_notifications():
        subscriber_key = request.args.to_dict().get('key') 
        return PushNotification().get_notifications(
            subscriber_key=subscriber_key
        )

    @app.route("/channels", methods=['POST', 'GET'])
    def create_channels():
        return PushNotification.create_channels(PushNotification)

    @app.route("/refresh", methods=['POST', 'GET'])
    def refresh():
        return PushNotification.refresh(PushNotification)

    @app.route("/subscribers", methods=['GET'])
    def subscribers():
        return Subscriber().subscribers()

    @app.route("/delete_subscribers", methods=['DELETE'])
    def delete_subscribers():
        subscriber_key = request.get_json()['key']
        return Subscriber().delete_subscribers(
            subscriber_key=subscriber_key
        )

    @app.route("/edit_subscribers", methods=['PUT'])
    def edit_subscribers():
        subscriber_key = request.args.to_dict().get('key')
        subscriber_info = request.get_json()['subscriber_info']
        subscribers = Subscriber().edit_subscribers(
            subscriber_info, subscriber_key=subscriber_key
        )
        return Response(status=200, response=subscribers)

    @app.route("/subscription/new", methods=['GET'])
    def new_subscription():
        return render_template('subscriptions.html')

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

    return app
