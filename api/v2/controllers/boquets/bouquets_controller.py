from flask import make_response, jsonify
from flask_restful import Resource
from api.v2.helpers.bouquets.bouquets_helper import (
    query_all_bouquets, refresh_bouquet_channels)


class Bouquets(Resource):
    def get(self):
        bouquets = query_all_bouquets()

        return make_response(jsonify({"bouquets": bouquets}), 200)


class RefreshChannels(Resource):
    def post(self, api_type, bouquet_id):
        response = make_response(
            jsonify(
                {'Error': 'Endpoint accepts only graphql_api/restful_api'}
            ), 404)
        if (api_type == 'restful_api') or (api_type == 'graphql_api'):
            refresh = refresh_bouquet_channels(api_type, bouquet_id)
            response = make_response(
                jsonify(refresh['response']), refresh['code'])

        return response
