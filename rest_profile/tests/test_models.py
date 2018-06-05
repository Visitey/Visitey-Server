# -*- coding:utf-8 -*-

#  Core Django imports
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import RequestFactory
# Third-party app imports
from rest_framework.test import APITestCase, APIClient

from rest_profile.models import Profile


class BaseTestCase(APITestCase):

    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.factory = RequestFactory()
        self.client = APIClient()
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def create_user(self, username, password, email_address):
        user = User.objects.create_user(username, password, email_address)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse202(self, response):
        self.assertEqual(response.status_code, 202)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse400(self, response):
        self.assertEqual(response.status_code, 400)

    def assertResponse401(self, response):
        self.assertEqual(response.status_code, 401)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)


class ProfileModelTests(BaseTestCase):

    def setUp(self):
        super(ProfileModelTests, self).setUp()

    def test_object_name(self):
        profile = Profile.objects.get(id=self.user_bob.profile.id)
        expected_object_name = '%s' % profile.pseudo
        self.assertEquals(expected_object_name, str(profile))

    def test_get_absolute_url(self):
        profile = Profile.objects.get(id=self.user_bob.profile.id)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(profile.get_absolute_url(), '/profile/' + str(self.user_bob.profile.id) + '/')
