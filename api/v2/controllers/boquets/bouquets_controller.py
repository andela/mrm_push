from flask import make_response, jsonify, request
from flask_restful import Resource

from api.v2.helpers.bouquets.bouquets_helper import query_all_bouquets, create_bouquet
from api.v2.utilities.validators import validate_bouquet_adding

class Bouquets(Resource):
    method_decorators = [validate_bouquet_adding]

    def get(self):
        bouquets = query_all_bouquets()
        return make_response(jsonify({"bouquets": bouquets}), 200)

    def post(self):
        request_data = request.get_json()
        _create_bouquet = create_bouquet(request_data)
        return make_response(jsonify({"data": _create_bouquet}), 201)
