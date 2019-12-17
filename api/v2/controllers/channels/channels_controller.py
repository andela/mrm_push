import os
import uuid

from flask import make_response, jsonify
from flask_restful import Resource, request
from googleapiclient.errors import HttpError

from api.v2.helpers.credentials import check_bouquet_credentials
from api.v2.helpers.channels.channels_helper import query_all_channels
from api.v2.models.channels.channels_model import Channels as channels_model
from api.v2.helpers.bouquets.bouquets_helper import query_bouquet
from api.v2.utilities.validators import validate_calendar_info


class Channels(Resource):
    def get(self):
        channels = query_all_channels()
        return make_response(jsonify({'channels': channels}), 200)

    def post(self):
        # Endpoint to add channels to a bouquet
        try:
            calendar = request.get_json()

            # Function call to validate channel data
            _calendar = validate_calendar_info(calendar)
            if _calendar.errors:
                return {'error': _calendar.errors}, 400

            # Function call to retrieve a bouquet
            bouquet = query_bouquet(calendar['bouquet_id'])
            if not bouquet:
                return {'error': f"bouquet with id={calendar['bouquet_id']} doesn't exist"}, 404

            if bouquet['should_refresh']:
                return {'error': "can't manually add calendar to this bouquet"}, 403

            bouquet_credentials = check_bouquet_credentials(bouquet)
            service = bouquet_credentials['service']

            channel = channels_model.query.filter_by(
                                   calendar_id=calendar['calendar_id']).first()

            if channel:
                return {'error': 'calendar already in the bouquet'}, 409

            event = service.events().watch(
                    calendarId=calendar['calendar_id'], body={
                        'id': str(uuid.uuid1()),
                        'type': 'web_hook',
                        'address': os.getenv('NOTIFICATION_URL')
                    }).execute()

            if event:
                # save calendar to the bouquet
                _channel = channels_model.save_channel(
                    channel_id=event['id'],
                    calendar_id=calendar['calendar_id'],
                    resource_id=event['resourceId'],
                    extra_atrributes=event['resourceUri'],
                    bouquet_id=calendar['bouquet_id'],
                    state='active')

            if _channel:
                return {'message': 'calendar added successfully'}, 200

        except HttpError as err:
            if err.resp.status == 404:
                return {'error': 'calendar not found'}, err.resp.status
            return {'error': err._get_reason()}, err.resp.status

        except Exception:
            return {'error': 'server error! please try again later'}, 500
