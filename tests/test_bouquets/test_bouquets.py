import json
from tests.base import BaseTestCase


class TestBouquets(BaseTestCase):
    def test_get_all_bouquets(self):
        response = self.app_test.get("/v2/bouquets")
        self.assertEqual(response.status_code, 200)

    def test_add_bouquet(self):
        # Should return 201 when valid data object is sent
        response = self.app_test.post("/v2/bouquets", data=json.dumps(self.bouquet_200),
                                      content_type='application/json')
        re = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(re["data"]["message"], "successfully added bouquet")

        # Should return 500 when no data object is sent
        response = self.app_test.post("/v2/bouquets")
        re = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(re["error"], "failed to add bouquet")

        # Should return 400 when valid field is missing
        response = self.app_test.post("/v2/bouquets", data=json.dumps(self.bouquet_400_missing_key),
                                      content_type='application/json')
        re = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(re["error"], "please provide 'refresh_url'")

        # Should return 400 when no empty strings are supplied
        response = self.app_test.post("/v2/bouquets", data=json.dumps(self.bouquet_400_null_string),
                                      content_type='application/json')
        re = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(re["error"], "bouquet name should have at least one character")

        # Should return 400 when no a numeral is supplied for a bouquet name instead of string
        response = self.app_test.post("/v2/bouquets", data=json.dumps(self.bouquet_400_bn_numeral),
                                      content_type='application/json')
        re = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(re["error"], "bouquet name should not be numeric")


