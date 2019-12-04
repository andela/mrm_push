import json

from unittest.mock import patch

from tests.base import BaseTestCase


class TestBouquets(BaseTestCase):
    def test_get_all_bouquets(self):
        # Should get all bouquets
        response = self.app_test.get('/v2/bouquets')

        self.assertEqual(response.status_code, 200)

    def test_adding_bouquet(self):
        # Should add bouquet
        response = self.app_test.post('/v2/bouquets', data=json.dumps(self.bouquet_201),
                                      content_type='application/json')
        re = json.loads(response.data.decode())

        self.assertEqual(re['data']['message'], 'successfully added bouquet')
        self.assertEqual(response.status_code, 201)

    def test_bouquet_400_missing_key(self):
        # Should return 400 when valid field is missing
        response = self.app_test.post('/v2/bouquets', data=json.dumps(self.bouquet_400_missing_key),
                                      content_type='application/json')
        re = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(re['error'], "please provide 'bouquet_name'")

    def test_bouquet_400_null_string(self):
        # Should return 400 when no empty strings are supplied
        response = self.app_test.post('/v2/bouquets', data=json.dumps(self.bouquet_400_null_string),
                                      content_type='application/json')
        re = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(re['errors']['bouquet_name'], ['empty values not allowed'])

    def test_bouquet_400_wrong_url(self):
        # Should return 400 when a wrong url is used
        response = self.app_test.post('/v2/bouquets', data=json.dumps(self.bouquet_400_wrong_url),
                                      content_type='application/json')
        re = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(re['error'], "please provide a valid url e.g 'https://re.com'")

    def test_bouquet_500(self):
        # Should return 500 when no data object is sent
        response = self.app_test.post('/v2/bouquets')
        re = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 500)
        self.assertEqual(re['error'], 'failed to add bouquet')
