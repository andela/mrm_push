import datetime

from flask import make_response, jsonify, request
from flask_restful import Resource
from api.v2.models.logs.logs_model import Logs as LogsModel
from api.v2.models.logs.logs_schema import LogsSchema


class Logs(Resource):
    def get(self):
        '''
        Function to get all logs from the database
        @return a list of logs
        '''
        try:
            get_logs = LogsModel.query.all()
            logs = 'No logs found'
            if get_logs:
                logs = LogsSchema(many=True).dump(get_logs)
                return make_response(jsonify({'logs': logs}), 200)
        except:
            return make_response(jsonify({'error': 'server error! please try again later'}), 500)


    @staticmethod
    def save_log(data):
        '''
        Function to save logs in the database
        '''
        try:
            LogsModel.save_log(timestamp = datetime.datetime.now(), calendar_id = data['calendar_id'],
                subscriber_name = data['subscriber_name'],
                subscription_method = data['subscription_method'],
                payload = data['payload'])
            return "log saved succesfully"
        except:
            return "unable to save log"
