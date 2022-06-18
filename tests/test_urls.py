from django.contrib.auth import get_user_model
from django.test import TestCase, Client


User = get_user_model()


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.browser_client_guest = Client()

        self.user = User.objects.create_user(username='UserAuth')
        self.browser_client_auth = Client()
        self.browser_client_auth.force_login(self.user)

    def test_homepage(self):
        """Test main page return status code 200 """
        response = self.browser_client_guest.get('/')
        self.assertEqual(response.status_code, 200)
