from helpers.credentials import Credentials
from flask import jsonify, request
from pyfcm import FCMNotification
from config import config
from models.calendar_model import Calendar
from utilities.utility import (update_entity_fields, stop_channel)
from apiclient import errors
import uuid
import requests
import os


config_name = os.getenv('APP_SETTINGS')
push_service = FCMNotification(api_key=os.getenv('FCM_API_KEY'))
api_token = os.getenv('USER_TOKEN')

notification_url = config.get(config_name).NOTIFICATION_URL
url = config.get(config_name).CONVERGE_MRM_URL


class PushNotification():

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
