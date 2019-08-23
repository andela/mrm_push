from tests.base import BaseTestCase


class TestChannels(BaseTestCase):
    def test_get_all_channels(self):
        response = self.app_test.get("/v2/channels")

        self.assertEqual(response.status_code, 200)
