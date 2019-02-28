import os
import uuid
import json

import requests
from apiclient import errors
from flask import jsonify, request
from pyfcm import FCMNotification
from pywebpush import webpush, WebPushException

from config import config
from helpers.credentials import Credentials
from models.calendar_model import Calendar
from models.subscribers_model import Subscriber
from utilities.utility import (update_entity_fields, stop_channel)

config_name = os.getenv('APP_SETTINGS')
push_service = FCMNotification(api_key=os.getenv('FCM_API_KEY'))
api_token = os.getenv('USER_TOKEN')
vapid_private_key = os.getenv("VAPID_PRIVATE_KEY")
vapid_email = os.getenv("VAPID_EMAIL")

notification_url = config.get(config_name).NOTIFICATION_URL
url = config.get(config_name).CONVERGE_MRM_URL


class PushNotification():
    def get_supported_platforms(self):
        supported_platforms = {
            "web": self.send_web_notification,
            "graphql": self.send_graphql_notification,
            "rest": self.send_rest_notification,
            "android": self.send_android_notification
        }

        return supported_platforms

    def refresh(self):
        rooms_query = (
            {"query": "{ allRooms { rooms { calendarId, firebaseToken } } }"})
        headers = {'Authorization': 'Bearer %s' % api_token}
        all_rooms = requests.post(url=url, json=rooms_query, headers=headers)

        rooms = all_rooms.json()['data']['allRooms']['rooms']
        for room in rooms:
            exact_calendar = Calendar.query.filter_by(
                calendar_id=room['calendarId']).first()
            if not exact_calendar:
                calendar = Calendar(calendar_id=room['calendarId'],
                                    firebase_token=room['firebaseToken'])
                calendar.save()
                continue

            if exact_calendar.firebase_token != room['firebaseToken']:
                update_entity_fields(exact_calendar,
                                     calendar_id=room['calendarId'],
                                     firebase_token=room['firebaseToken'])
                exact_calendar.save()

        data = {
            "message": "Calendars saved successfully"
        }
        response = jsonify(data)

        return response

    def create_channels(self):
        request_body = {
            "id": None,
            "type": "web_hook",
            "address": notification_url
        }
        service = Credentials.set_api_credentials(self)
        calendars = Calendar.query.all()
        channels = []

        for calendar in calendars:
            request_body['id'] = str(uuid.uuid4())
            stop_channel(service, calendar.channel_id, calendar.resource_id)

            try:
                channel = service.events().watch(
                    calendarId=calendar.calendar_id,
                    body=request_body).execute()
            except errors.HttpError as error:
                print('An error occurred', error)
                continue

            update_entity_fields(
                calendar, channel_id=channel['id'],
                resource_id=channel['resourceId'])
            calendar.save()
            channels.append(channel)

        response = jsonify(channels)
        return response

    def send_notifications(self):
        exact_calendar = Calendar.query.filter_by(
            resource_id=request.headers['X-Goog-Resource-Id']).first()
        if exact_calendar.firebase_token:
            result = push_service.notify_single_device(
                registration_id=exact_calendar.firebase_token,
                message_body="success")
            return jsonify(result)

        data = {
            "message": "Notification received but no registered device"
        }
        response = jsonify(data)

        return response

    def send_web_notification(self, subscription_info, calendar_id):
        subscription_info = json.loads(subscription_info)
        try:
            webpush(
                subscription_info=subscription_info,
                data=str(calendar_id),
                vapid_private_key=vapid_private_key,
                vapid_claims={
                    "sub": "mailto:" + vapid_email
                }
            )
        except WebPushException as exception:
            print(exception)

    def send_rest_notification(self, subscriber_url, calendar_id):
        try:
            requests.post(url=subscriber_url, json=calendar_id)
        except Exception as e:
            print(e)

    def send_graphql_notification(self, subscriber_url, calendar_id):
        calendar_id = str(calendar_id)
        notification_mutation = "mutation{mrmNotification(calendarId:\"" + calendar_id + "\"){message}}"
        try:
            requests.post(url=subscriber_url, json={'query': notification_mutation})
        except Exception as e:
            print(e)

    def send_android_notification(self, firebase_token, calendar_id):
        push_service.notify_single_device(
            registration_id=firebase_token,
            message_body=calendar_id)

    def send_notifications_to_subscribers(self):
        calendar = Calendar.query.filter_by(
            resource_id=request.headers['X-Goog-Resource-Id']).first()
        calendar_id = calendar.calendar_id
        subscribers = Subscriber.query.filter(Subscriber.calendars.any(
            calendar_id=calendar_id)).all()
        supported_platforms = self.get_supported_platforms()
        for subscriber in subscribers:
            platform = subscriber.platform
            subscriber_url = subscriber.subscription_info
            supported_platforms[platform](subscriber_url, calendar_id)

    def subscribe(self, subscriber_info):
        suported_platforms = self.get_supported_platforms().keys()
        if not subscriber_info["platform"] in suported_platforms:
            return "We currently do not support this platform"
        if subscriber_info["platform"] == "web":
            subscriber_info["subscription_info"] = json.dumps(subscriber_info["subscription_info"])
        calendar_ids = subscriber_info.get("calendars")
        if not calendar_ids:
            calendars = Calendar.query.all()
            calendar_ids = [calendar.id for calendar in calendars]

        subscriber_key = str(uuid.uuid4())
        subscriber_info["subscriber_key"] = subscriber_key
        subscriber = Subscriber(
            platform=subscriber_info["platform"],
            subscription_info=subscriber_info["subscription_info"],
            subscribed=True,
            subscriber_key=subscriber_key
        )
        for calendar_id in calendar_ids:
            calendar = Calendar.query.filter_by(id=calendar_id).first()
            subscriber.calendars.append(calendar)
        subscriber.save()

        return subscriber_info
