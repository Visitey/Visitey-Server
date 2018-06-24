# -*- coding:utf-8 -*-

#  Core Django imports
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.core.cache import cache
from django.test import RequestFactory
# Third-party app imports
from rest_framework.test import APITestCase, APIClient

from rest_geo.models import PointOfInterest, Route


class BaseTestCase(APITestCase):

    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.poi = PointOfInterest.objects.create(title='Test', description='Test',
                                                  location=GEOSGeometry('POINT(0 0)', srid=4326))
        self.route = Route.objects.create(title='RouteTest', description='Test')
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


class PointOfInterestModelTests(BaseTestCase):

    def setUp(self):
        super(PointOfInterestModelTests, self).setUp()

    def test_object_name(self):
        expected_object_name = 'Test'
        self.assertEquals(expected_object_name, str(self.poi))

    def test_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEquals(self.poi.get_absolute_url(), '/pointofinterest/' + str(self.poi.id) + '/')


class RouteModelTests(BaseTestCase):

    def setUp(self):
        super(RouteModelTests, self).setUp()

    def test_object_name(self):
        expected_object_name = 'RouteTest'
        self.assertEquals(expected_object_name, str(self.route))

    def test_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEquals(self.route.get_absolute_url(), '/route/' + str(self.route.id) + '/')
