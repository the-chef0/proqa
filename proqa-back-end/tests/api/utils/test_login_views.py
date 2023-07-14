from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from social_django.models import UserSocialAuth


class TestLoginViews(TestCase):
    """ Test views"""

    def setUp(self):
        """ Set up for tests"""
        # usernames and password
        self.user_name = 'testuser'
        self.admin_user_name = 'admin'
        self.password = '12345'

        # create users
        self.user = get_user_model().objects.\
            create_user(username=self.user_name, password=self.password)
        # connect user to social auth
        self.social_auth_user = UserSocialAuth.objects.\
            create(user=self.user, provider='oidc', uid='123456')

        # create admin user
        self.admin_user = get_user_model().objects.\
            create_superuser(username=self.admin_user_name, password=self.password)

        # create client to make requests
        self.client = Client()

    def test_get_username(self):
        """ Test get username view"""
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('get_username'))
        self.assertEqual(response.status_code, 200)
        # check that uid is returned
        self.assertEqual(response.json()['username'], '123456')

    def test_csrf_token_view(self):
        """ Test csrf token view"""
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('get_csrf_token'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrf_token', response.json())
        self.assertIsNotNone(response.json()['csrf_token'])

    def test_check_login_status_user_logged_in(self):
        """ Test check login status view for a logged in normal user"""
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('check_login_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_logged_in'])
        self.assertFalse(response.json()['is_admin'])

    def test_check_login_status_admin_logged_in(self):
        """ Test check login status view for a logged in admin user"""
        self.client.login(username=self.admin_user_name, password=self.password)
        response = self.client.get(reverse('check_login_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_logged_in'])
        self.assertTrue(response.json()['is_admin'])

    def test_check_login_status_not_logged_in(self):
        """ Test check login status view for a user who is not logged in"""
        response = self.client.get(reverse('check_login_status'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['is_logged_in'])
        self.assertFalse(response.json()['is_admin'])

    def test_logout_view(self):
        """ Test logout view"""
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Logout successful')
        # Check if the user is logged out by trying to access a view that requires login
        response = self.client.get(reverse('get_username'))
        self.assertEqual(response.status_code, 302)  # Should redirect to the login page
