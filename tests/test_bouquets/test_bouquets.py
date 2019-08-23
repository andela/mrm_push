from tests.base import BaseTestCase


class TestBouquets(BaseTestCase):
    def test_get_all_bouquets(self):
        response = self.app_test.get("/v2/bouquets")

        self.assertEqual(response.status_code, 200)
