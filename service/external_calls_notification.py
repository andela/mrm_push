import requests
import os
import json

from flask import Flask
from pyfcm import FCMNotification

from config import config
from utilities.utility import save_to_db
import celery

config_name = os.getenv('APP_SETTINGS')
push_service = FCMNotification(api_key=os.getenv('FCM_API_KEY'))
api_token = os.getenv('USER_TOKEN')

notification_url = config.get(config_name).NOTIFICATION_URL
url = config.get(config_name).CONVERGE_MRM_URL
app = Flask(__name__)


class ExternalCallsNotifications():
    #notify a single device and save notifications
    @celery.task(name='push_notification-single-device')
    def notify_device(firebase_token, calendar_id):
        try:
            results = push_service.notify_single_device(
                registration_id = firebase_token,
                message_body="success")
            result = {}
            result['results'] = results['results']
            result['subscriber_info'] = firebase_token
            result['platform'] = 'android'
            result['calendar_id'] = calendar_id
            save_to_db(result)
            return results
        except Exception as error:
            results = error
            result = {}
            result['results'] = results
            result['subscriber_info'] = firebase_token
            result['platform'] = 'android'
            result['calendar_id'] = calendar_id
            save_to_db(result)
            return error

     
    #update the backend API method
    @celery.task(name='push_notification-update-backend')
    def update_backend(calendar_id):
        try:
            notify_api_mutation = (
                {
                    'query':
                        """
                        mutation {
                            mrmNotification ( calendarId: \"%s\" ) {
                                message
                            }
                        }
                        """ % calendar_id
                }
            )
            headers = {'Authorization': 'Bearer %s' % api_token}
            requests.post(url=url, json=notify_api_mutation, headers=headers)
        except Exception as error:
            return error    

