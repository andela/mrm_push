import json

from unittest.mock import patch

from tests.base import BaseTestCase

from api.v2.controllers.bouquets.bouquets_controller import Bouquets

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
        
    def test_delete_bouquet(self):
        # Should return 404 when a bouquets is not found
        response = self.app_test.delete("/v2/bouquets?bouquet_id=100")
        self.assertTrue(b"The bouquet you want to delete is not found" in response.data)
        self.assertEqual(response.status_code, 404)

    def test_delete_bouquet_correctly(self):
        # Should return 200 when a bouquet was deleted
        response = self.app_test.delete("/v2/bouquets?bouquet_id=1")
        self.assertTrue(b"The bouquet was deleted successfully" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_bouquet_with_invalid_id(self):
        # Should return 400 when a bouquet_id is not integer
        response = self.app_test.delete("/v2/bouquets?bouquet_id=mmm")
        self.assertTrue(b"The bouquet id should be an integer. Try again" in response.data)
        self.assertEqual(response.status_code, 400)
