'''Test api endpoints'''
import json
import unittest
from unittest.mock import patch

from app import create_app
from api.v1.service.push_notification import PushNotification


class api_test_case(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def tearDown(self):
        pass

    @patch("api.v1.service.push_notification.PushNotification.subscribe", spec=True)
    def test_subscribe(self, mock_get_json):
        subscription_info = json.dumps({
            "subscriber_info": {
                "platform": "web",
                "subscription_info": "url",
                "calendars": []
            }
        })
        mock_get_json.return_value = {'platform': 'web', 'subscription_info': 'url', 'calendars': [],
                                      'subscriber_key': '98261828-b45d-407e-9684-8ed22f95509d'}
        response = self.client().post("/v1/subscription", data=subscription_info, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    @patch("requests.post", spec=True)
    def test_send_rest_notification(self, mock_request):
        PushNotification().send_rest_notification("url", "calendar_id")
        mock_request.assert_called_with(json='calendar_id', url='url')

    @patch("requests.post", spec=True)
    def test_send_graphql_notification(self, mock_request):
        PushNotification().send_graphql_notification("url", "calendar_id")
        mock_request.assert_called_with(json={'query': 'mutation{mrmNotification(calendarId:"calendar_id"){message}}'}, url='url')


if __name__ == "__main__":
    unittest.main()
