from tests.base import BaseTestCase
from api.v2.controllers.channels.channels_controller import Channels
from flask import json


class TestChannels(BaseTestCase, Channels):
    def test_get_all_channels(self):
        response = self.app_test.get("/v2/channels")

        self.assertEqual(response.status_code, 200)

    # test add calendar to unexisting bouquet/bouquet_id
    def test_add_calendar_to_unexsting_bouquet(self):
        payload = {
                    "calendar_id": "emileagimana@andela.com",
                    "bouquet_id": 100
        }
        response = self.app_test.post("/v2/channels", data=json.dumps(payload),
                                      content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['error'], 'bouquet with id=100 doesn\'t exist')
        self.assert404(response)

    # test add same calendar to a bouquet
    def test_add_calendar_twice(self):
        payload = {
            "calendar_id": "emilereas@gmail.com",
            "bouquet_id": 2
        }
        response = self.app_test.post("/v2/channels", data=json.dumps(payload),
                                      content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['error'], 'calendar already in the bouquet')
        self.assertEqual(response.status_code, 409)

    # test add invalid calendar
    def test_add_unknown_calendar_id(self):
        payload = {
            "calendar_id": "abc@gmail.com",
            "bouquet_id": 1
        }
        response = self.app_test.post("/v2/channels", data=json.dumps(payload),
                                      content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['error'], 'server error! please try again later')
        self.assert500(response)

    # test for adding invalid calendar to a bouquet
    # eg. missing fields or empty request body
    def test_add_invalid_channel(self):
        response = self.app_test.post("/v2/channels", data=json.dumps({}),
                                      content_type='application/json')
        response_payload = {
            'bouquet_id': ['required field'],
            'calendar_id': ['required field']
        }
        res = json.loads(response.data.decode())
        self.assertEqual(res['error'], response_payload)
        self.assert_400(response)

    def test_no_request_channel(self):
        response = self.app_test.post("/v2/channels")
        self.assert500(response)
