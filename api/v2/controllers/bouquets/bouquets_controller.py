from flask import make_response, jsonify, request
from flask_restful import Resource

from api.v2.helpers.bouquets.bouquets_helper import query_all_bouquets
from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel
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
