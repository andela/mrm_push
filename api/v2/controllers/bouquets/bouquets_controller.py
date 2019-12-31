import requests
import datetime

from flask import make_response, jsonify, request
from flask_restful import Resource

from api.v2.helpers.bouquets.bouquets_helper import query_all_bouquets, query_bouquet
from api.v2.helpers.channels.channels_helper import query_channel
from api.v2.helpers.subscriber.subscriber_helper import get_subscribers
from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel
from api.v2.models.logs.logs_model import Logs
from api.v2.utilities.validators import validate_bouquet_adding
from api.v2.helpers.credentials import check_bouquet_credentials


class Bouquets(Resource):

    method_decorators = [validate_bouquet_adding]

    def get(self):
        bouquets = query_all_bouquets()
        return make_response(jsonify({'bouquet': bouquets}), 200)

    def post(self):
        data = request.get_json()
        redirect_uris = ''
        if 'should_refresh' not in data.keys():
            data['should_refresh'] = False
        if 'refresh_url' not in data.keys():
            data['refresh_url'] = 'none'
        for i in data['redirect_uris']:
            redirect_uris += f'{i} '
        data['redirect_uris'] = redirect_uris
        credentials = check_bouquet_credentials(data)  # get refresh token
        BouquetsModel.add_bouquet(bouquet_name=data['bouquet_name'], client_id=data['client_id'],
                                  client_secret=data['client_secret'], auth_uri=data['auth_uri'],
                                  token_uri=data['token_uri'], redirect_uris=data['redirect_uris'],
                                  refresh_url=data['refresh_url'], should_refresh=data['should_refresh'],
                                  refresh_token=credentials['refresh_token'])
        return make_response(jsonify({'data': {'message': 'successfully added bouquet',
                                               'bouquet': data}}), 201)
    
    def delete(self):
        bouquet_id = request.args['bouquet_id']
        if not bouquet_id.isdigit():
            return make_response(jsonify({'message': 'The bouquet id should be an integer. Try again'}), 400)
        bouquet = query_bouquet(bouquet_id)
        if not bouquet:
            return make_response(jsonify({'message': 'The bouquet you want to delete is not found'}), 404)
        BouquetsModel.delete_bouquet(BouquetsModel, bouquet_id)
        return make_response(jsonify({'message': 'The bouquet was deleted successfully'}), 200)

        
class SendNotifications(Resource):
    
    def post(self):
            """function to receive notifications and send them to subscriber"""
            resource_id = request.headers['X-Goog-Resource-ID']
            channel = query_channel(resource_id)
            if not channel:
                return make_response(jsonify({'message': 'Channel not found'}), 404)
            
            bouquet_id = channel['bouquet_id']
            subscribers = get_subscribers(bouquet_id)
            if not subscribers:
                return make_response(jsonify({'message': 'Subscribers not found'}), 404)
            
            for subscriber in subscribers:
                calendar_id = channel['calendar_id']
                notification_url = subscriber['notification_url']
                results = requests.post(url=notification_url, json=calendar_id)
                Logs.save_log(timestamp = datetime.datetime.now(),
                                    calendar_id=calendar_id,
                                    subscriber_name = subscriber['subscriber_name'],
                                    subscription_method = subscriber['subscription'].name,
                                    payload = results.status_code)
            
            return make_response(jsonify({'message': 'Notifications sent'}), 200)
