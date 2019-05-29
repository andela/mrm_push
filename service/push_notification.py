import uuid
import requests
import os
import json
import ast
import datetime

from models.calendar_model import Calendar
from models.notification_model import Notification
from flask import jsonify, request, render_template
from pyfcm import FCMNotification
from pywebpush import webpush, WebPushException

from config import config
from helpers.credentials import Credentials
from utilities.utility import update_entity_fields, save_to_db, stop_channel
from apiclient import errors


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

    def update_firebase_token(self, calendar_id, firebase_token):
        exact_calendar = Calendar.query.filter_by(
            calendar_id=calendar_id).first()
        update_entity_fields(exact_calendar,
                             calendar_id=calendar_id,
                             firebase_token=firebase_token)
        exact_calendar.save()
        return "OK"

    def refresh(self):
        rooms_query = (
            {"query": "{ allRooms { rooms { calendarId, firebaseToken } } }"})
        headers = {'Authorization': 'Bearer %s' % api_token}
        all_rooms = requests.post(url=url, json=rooms_query, headers=headers)

        rooms = all_rooms.json()['data']['allRooms']['rooms']
        selected_calendar = {}
        selected_calendar_key = ''
        for room in rooms:
            exact_calendar = Calendar.query.filter_by(
                calendar_id=room['calendarId']).first()
            if not exact_calendar:
                Calendar(calendar_id=room['calendarId'],
                         firebase_token=room['firebaseToken']).save()
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
        calendar = {}
        calendars = Calendar.query.all()
        channels = []

        for calendar in calendars:
            request_body['id'] = str(uuid.uuid4())
            stop_channel(
                service, calendar.channel_id, calendar.resource_id)

            try:
                channel = service.events().watch(
                    calendarId=calendar.calendar_id,
                    body=request_body).execute()
            except errors.HttpError as error:
                print('An error occurred', error)
                continue

            update_entity_fields(calendar, channel_id=channel['id'],
                                 resource_id=channel['resourceId'])
            calendar.save()
            channels.append(channel)

        response = jsonify(channels)
        return response

    def send_notifications(self):
        exact_calendar = Calendar.query.filter_by(
            resource_id=request.headers['X-Goog-Resource-Id']).first()

        if exact_calendar.firebase_token:
            # results = push_service.notify_single_device(
            #     registration_id=exact_calendar.firebase_token,
            #     message_body="success")
            result = {}
            result['results'] = "results['results']"
            result['subscriber_info'] = "selected_calendar['firebase_token']"
            result['platform'] = 'android'
            result['time'] = datetime.datetime.now().replace(
                second=0, microsecond=0)

            Notification(results=result['results'],
                         subscriber_info=result['subscriber_info'],
                         platform=result['platform'], time=result['time']).save()
            return jsonify(result)

        data = {
            "message": "Notification received but no registered device"
        }
        response = jsonify(data)

        return response

    def send_web_notification(self, subscriber, calendar_id):
        subscription_info = json.loads(subscriber['subscription_info'])
        try:
            data = webpush(
                subscription_info=subscription_info,
                data=str(calendar_id),
                vapid_private_key=vapid_private_key,
                vapid_claims={
                    "sub": "mailto:" + vapid_email
                }
            )
            result = {}
            result['results'] = data.status_code
            result['platform'] = subscriber['platform']
            result['subscriber_info'] = subscriber['subscriber_key']
            save_to_db(result)
        except WebPushException as exception:
            print(exception)

    def send_rest_notification(self, subscriber_url, calendar_id):
        try:
            result = requests.post(url=subscriber_url, json=calendar_id)
            save_to_db(result)
        except Exception as e:
            print(e)

    def send_graphql_notification(self, subscriber_url, calendar_id):
        calendar_id = str(calendar_id)
        notification_mutation = "mutation{mrmNotification(calendarId:\"" + \
            calendar_id + "\"){message}}"
        try:
            result = requests.post(url=subscriber_url, json={
                'query': notification_mutation})
            save_to_db(result)
        except Exception as e:
            print(e)

    def send_android_notification(self, firebase_token, calendar_id):
        results = push_service.notify_single_device(
            registration_id=firebase_token,
            message_body=calendar_id)
        result = {}
        result['results'] = results['results']
        result['subscriber_info'] = firebase_token
        result['platform'] = 'android'
        save_to_db(result)

    def subscribe(self, subscriber_info):
        suported_platforms = self.get_supported_platforms().keys()
        if not subscriber_info["platform"] in suported_platforms:
            return "We currently do not support this platform"
        if subscriber_info["platform"] == "web":
            subscriber_info["subscription_info"] = json.dumps(
                subscriber_info["subscription_info"])
        subscriber_calendar_ids = subscriber_info.get("calendars")
        calendar_ids = subscriber_calendar_ids
        if not subscriber_calendar_ids:
            calendar_ids = []
            for key in db.keys('*Calendar*'):
                calendar = db.hgetall(key)
                calendar_ids.append(key)

        subscriber_key = str(uuid.uuid4())
        subscriber_info["subscriber_key"] = subscriber_key
        subscriber_details = {'platform': subscriber_info["platform"], 'subscription_info': subscriber_info[
            "subscription_info"], "subscribed": "True", "subscriber_key": subscriber_key}
        key = len(db.keys('*Subscriber*')) + 1
        db.hmset('Subscriber:' + str(key), subscriber_details)
        calendars = []
        for calendar_id in calendar_ids:
            calendar = {}
            for calendar_key in db.keys('*Calendar*'):
                each_calendar = db.hgetall(calendar_key)
                if each_calendar['calendar_id'] == calendar_id:
                    calendar = each_calendar
                    subscibers_list = []
                    if 'subscribers_list' in calendar.keys():
                        subscibers_list = calendar['subscribers_list'].strip(
                            '"')
                        subscibers_list = ast.literal_eval(subscibers_list)
                        subscibers_list.append(subscriber_details)
                    else:
                        subscibers_list.append(subscriber_details)
                    db.hmset(calendar_key, {
                             'subscribers_list': str(subscibers_list)})
                    calendar = db.hgetall(calendar_key)
                    calendars.append(calendar)
                    break
        db.hmset('Subscriber:' + str(key), {'calendars': str(calendars)})
        return subscriber_info

    def get_notifications(self):
        notifications = Notification.query.all()
        print(notifications)
        return render_template(
            'log.html',
            result=notifications
        )
