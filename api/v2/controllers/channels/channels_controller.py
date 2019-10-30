from flask import make_response, jsonify
from flask_restful import Resource
from api.v2.helpers.channels.channels_helper import query_all_channels


class Channels(Resource):
    def get(self):
        channels = query_all_channels()
        return make_response(jsonify({"channels": channels}), 200)
