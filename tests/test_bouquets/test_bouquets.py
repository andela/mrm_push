from unittest.mock import patch
from tests.base import BaseTestCase


class TestBouquets(BaseTestCase):
    def test_get_all_bouquets(self):
        response = self.app_test.get("/v2/bouquets")

        self.assertEqual(response.status_code, 200)

    @patch("api.v2.helpers.bouquets.bouquets_helper.graphql_channels")
    def test_refresh_graphql_channels(self, mock_get):
        channels = [{
            "calendarId":
            "andela.com_3734303034@resource.calendar.google.com",
            "firebaseToken": ""
        }]
        mock_get.return_value = channels
        response = self.app_test.post("/v2/refresh/graphql_api/1")

        self.assertEqual(response.status_code, 200)

    def test_refresh_with_invalid_graphql_url(self):
        response = self.app_test.post("/v2/refresh/graphql_api/1")

        self.assertEqual(response.status_code, 424)

    @patch("api.v2.helpers.bouquets.bouquets_helper.restful_channels")
    def test_refresh_restful_channels(self, mock_get):
        channels = [{
            "calendarId":
            "andela.com_3734303034@resource.calendar.google.com",
            "firebaseToken": ""
        }]
        mock_get.return_value = channels
        response = self.app_test.post("/v2/refresh/restful_api/1")

        self.assertEqual(response.status_code, 200)

    def test_refresh_with_invalid_restful_url(self):
        response = self.app_test.post("/v2/refresh/restful_api/1")

        self.assertEqual(response.status_code, 424)
