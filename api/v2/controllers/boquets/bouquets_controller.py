from flask import make_response, jsonify
from flask_restful import Resource
from api.v2.helpers.bouquets.bouquets_helper import query_all_bouquets


class Bouquets(Resource):
    def get(self):
        bouquets = query_all_bouquets()

        return make_response(jsonify({"bouquets": bouquets}), 200)
