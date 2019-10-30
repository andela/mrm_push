import json

from tests.base import BaseTestCase
from api.v2.controllers.logs.logs_controller import Logs

class TestLogs(BaseTestCase, Logs):
    '''
    test for getting all logs
    '''
    def test_get_logs(self):
        response = self.app_test.get("/v2/logs")

        self.assertEqual(response.status_code, 200)


    '''
    test for adding log
    '''
    def test_add_log(self):
        data = {
            "calendar_id" : 1,
            "subscriber_name" : "Andela",
            "subscription_method" : "method-1",
            "payload" : "good date"
        }
        response = self.save_log(data)
        self.assertEqual(response, 'log saved succesfully')

    '''
    test for adding log with an empty dictionary
    '''
    def test_add_invalid_log(self):
        response = self.save_log({})
        self.assertEqual(response, 'unable to save log')

