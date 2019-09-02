import json
import os
from flask import Blueprint, render_template, request, Response
from .service.push_notification import PushNotification

api_v1 = Blueprint('mrmpush', __name__, url_prefix="/v1")

vapid_public_key = os.getenv("VAPID_PUBLIC_KEY")


@api_v1.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@api_v1.route("/notifications", methods=['POST', 'GET'])
def calendar_notifications():
    PushNotification().send_notifications_to_subscribers()
    return PushNotification.send_notifications(PushNotification)


@api_v1.route("/channels", methods=['POST', 'GET'])
def create_channels():
    return PushNotification.create_channels(PushNotification)


@api_v1.route("/refresh", methods=['POST', 'GET'])
def refresh():
    return PushNotification.refresh(PushNotification)


@api_v1.route("/token", methods=['POST', 'GET'])
def update_firebase_token():
    calendar_id = request.args.get('calendar_id')
    firebase_token = request.args.get('firebase_token')
    return PushNotification.update_firebase_token(PushNotification, calendar_id, firebase_token)


@api_v1.route("/get_notifications", methods=['GET'])
def get_notifications():
    return PushNotification().get_notifications()


@api_v1.route("/subscription", methods=['POST', 'GET'])
def subscribe():
    if request.method == "GET":
        return Response(response=json.dumps({"public_key": vapid_public_key}),
                        headers={"Access-Control-Allow-Origin": "*"},
                        content_type="application/json"
                        )
    subscription_info = request.get_json()["subscriber_info"]
    subscription = PushNotification().subscribe(subscription_info)
    return Response(status=201, response=json.dumps(subscription))


@api_v1.route("/googledb635995d37deb01.html", methods=['GET'])
def verify_push_url():
    return render_template("googledb635995d37deb01.html")


@api_v1.route("/delete_room", methods=['DELETE'])
def delete_room():
    calendar_id = request.args.get('calendar_id')
    return PushNotification().delete_room(calendar_id)


@api_v1.route("/add_room", methods=['GET', 'POST'])
def add_room():
    calendar_id = request.args.get('calendar_id')
    firebase_token = request.args.get('firebase_token')
    return PushNotification().add_room(calendar_id, firebase_token)
