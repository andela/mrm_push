import uuid
import requests
import os
import json
import ast

from helpers.database import db
from flask import jsonify, request, render_template
from pyfcm import FCMNotification
from pywebpush import webpush, WebPushException

from config import config
from helpers.credentials import Credentials
from utilities.utility import stop_channel, save_to_db
from apiclient import errors
from helpers.calendar import update_calendar


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

    @staticmethod
    def get_endpoint(request_data=None):
        """ returns an endpoint that queries all subscriber rooms
        """
        all_endpoints = []
        subscriber_key = request_data['subscriber_key'] if request_data else None

        for key in db.keys('*Subscriber*'):
            subscribers = db.hgetall(key)
            if subscribers['subscriber_key'] == subscriber_key:
                return subscribers['calendar_ids_endpoint']

            all_endpoints.append(subscribers['calendar_ids_endpoint'])
        return all_endpoints

    @staticmethod
    def update_db(query, headers, sub_key=None):
        """ updates the Radis database with calendar_ids from the converge db
         :params
            - query, headers, sub_key
        """
        all_rooms = requests.post(url=url, json={"query": query}, headers=headers)

        endpoint, query_obj = query.split('{ ')[1].strip(), query.split('{ ')[2].strip()
        rooms = all_rooms.json()['data'][endpoint][query_obj]

        for key in db.keys('*Subscriber*'):
            subscribers = db.hgetall(key)
            if subscribers['subscriber_key'] == sub_key:
                db.hmset(key, {'calendars': str(rooms)})

        keys = db.keys('*Calendar*')
        calendars = [(key, db.hgetall(key)) for key in keys]
        room_calender_ids = set([room['calendarId'] for room in rooms])
        calendar_ids = set([calendar[1]['calendar_id'] for calendar in calendars])

        common_calendar_ids = room_calender_ids & calendar_ids
        for calendar in calendars:
            if calendar[1]['calendar_id'] in common_calendar_ids:
                update_existing_calendars(rooms, calendar[1], key)

        for room in rooms:
            if room['calendarId'] not in common_calendar_ids:
                update_calendar({}, '', room)

    def refresh(self, subscriber_key=None):
        """ Called by the refresh endpoint to update the Radis database
        both when a subscriber_key is passed and when not passed
        """
        headers = {'Authorization': 'Bearer %s' % api_token}
        if subscriber_key:
            query = PushNotification.get_endpoint(
                request_data={'subscriber_key': subscriber_key})
            PushNotification.update_db(query, headers, sub_key=subscriber_key)
            return jsonify({"message": "Calendars saved successfully"})

        else:
            queries = PushNotification.get_endpoint()
            if not queries:
                return jsonify({"error": "No endpoint found in database"})
            for query in queries:
                PushNotification.update_db(query, headers)
            return jsonify({"message": "Calendars saved successfully"})

    def create_channels(self):
        request_body = {
            "id": None,
            "type": "web_hook",
            "address": notification_url
        }
        service = Credentials.set_api_credentials(self)
        calendars = []
        channels = []
        for key in db.keys('*Calendar*'):
            calendar = db.hgetall(key)
            calendar['key'] = key
            calendars.append(calendar)

        for calendar in calendars:
            request_body['id'] = str(uuid.uuid4())
            if not 'channel_id' in calendar.keys():
                calendar['channel_id'] = ''
            if not 'resource_id' in calendar.keys():
                calendar['resource_id'] = ''
            stop_channel(service, calendar['channel_id'], calendar['resource_id'])

            try:
                channel = service.events().watch(
                    calendarId=calendar['calendar_id'],
                    body=request_body).execute()
            except errors.HttpError as error:
                print('An error occurred', error)
                continue

            db.hmset(calendar['key'], {'channel_id': channel['id'], 'resource_id': channel['resourceId']})
            channels.append(channel)

        response = jsonify(channels)
        return response

    def send_notifications(self):
        selected_calendar = {}
        for key in db.keys('*Calendar*'):
            calendar = db.hgetall(key)
            if 'resource_id' in calendar and calendar['resource_id'] == request.headers['X-Goog-Resource-Id']:
                selected_calendar = calendar
                break
        if 'firebase_token' in selected_calendar.keys():
            results = push_service.notify_single_device(
                registration_id=selected_calendar['firebase_token'],
                message_body="success")
            result = {}
            result['results'] = results['results']
            result['subscriber_info'] = selected_calendar['firebase_token']
            result['platform'] = 'android'
            save_to_db(result)
            return jsonify(results)

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
        notification_mutation = "mutation{mrmNotification(calendarId:\"" + calendar_id + "\"){message}}"
        try:
            result = requests.post(url=subscriber_url, json={'query': notification_mutation})
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

    def send_notifications_to_subscribers(self, sub_key):
        calendar_id = ''
        calendars = []
        for key in db.keys('*Calendar*'):
            each_calendar = db.hgetall(key)
            if 'resource_id' in each_calendar and each_calendar['resource_id'] == request.headers['X-Goog-Resource-Id']:
                calendar_id = each_calendar['calendar_id']
                calendars.append(calendar_id)
                break
        if sub_key in db.keys('*Subscriber*'):
            subscriber = db.hgetall(sub_key)
            supported_platforms = self.get_supported_platforms()
            platform = subscriber['platform']
            subscriber_url = subscriber['subscription_info']
            supported_platforms[platform](subscriber_url, calendar_id)

    def subscribe(self, subscriber_info):
        suported_platforms = self.get_supported_platforms().keys()
        if not subscriber_info["platform"] in suported_platforms:
            return "We currently do not support this platform"
        if subscriber_info["platform"] == "web":
            subscriber_info["subscription_info"] = json.dumps(subscriber_info["subscription_info"])
        subscriber_calendar_ids = subscriber_info.get("calendars")
        calendar_ids = subscriber_calendar_ids
        if not subscriber_calendar_ids:    
            calendar_ids = []
            for key in db.keys('*Calendar*'):
                calendar = db.hgetall(key)
                calendar_ids.append(key)

        subscriber_key = str(uuid.uuid4())
        subscriber_info["subscriber_key"] = subscriber_key
        subscriber_details = {
            "platform": subscriber_info["platform"],
            "subscription_info": subscriber_info["subscription_info"],
            "calendar_ids_endpoint": subscriber_info["calendar_ids_endpoint"],
            "subscribed": "True",
            "subscriber_key": subscriber_key}
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
                        subscibers_list = calendar['subscribers_list'].strip('"')
                        subscibers_list = ast.literal_eval(subscibers_list)
                        subscibers_list.append(subscriber_details)
                    else:
                        subscibers_list.append(subscriber_details)
                    db.hmset(calendar_key, {'subscribers_list': str(subscibers_list)})
                    calendar = db.hgetall(calendar_key)
                    calendars.append(calendar)
                    break
        db.hmset('Subscriber:' + str(key), {'calendars': str(calendars)})
        return subscriber_info

    def get_notifications(self):
        notifications = []
        for key in db.keys('*Notification*'):
            notification = db.hgetall(key)
            notifications.append(notification)
        return render_template(
            'log.html',
            result=notifications
        )


def update_existing_calendars(rooms, selected_calendar, selected_calendar_key):
    """ Update the Redis database for already existing calendars
         :params
            - rooms, selected_calendar, selected_calendar_key
         :returns: None
    """
    for room in rooms:
        update_calendar(selected_calendar, selected_calendar_key, room)
