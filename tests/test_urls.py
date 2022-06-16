from django.test import TestCase, Client


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser_client_guest = Client()

    def test_homepage(self):
        response = self.browser_client_guest.get('/')
        self.assertEqual(response.status_code, 200)
