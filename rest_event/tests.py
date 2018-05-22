from django.contrib.auth.models import User
from django.test import RequestFactory
from django.utils.http import urlencode
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from rest_event.models import Event
from rest_event.serializers import EventSerializer


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    """Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search', 'Bob'})
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class BaseTestCase(APITestCase):
    def setUp(self):
        """
        Setup initial user

        """
        self.user_pw = 'Alibaba'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.user_steve = self.create_user('steve', 'steve@steve.com', self.user_pw)
        self.user_susan = self.create_user('susan', 'susan@susan.com', self.user_pw)
        self.user_amy = self.create_user('amy', 'amy@amy.amy.com', self.user_pw)
        self.factory = RequestFactory()
        self.client = APIClient()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, password, email_address):
        user = User.objects.create_user(username, password, email_address)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse201(self, response):
        self.assertEqual(response.status_code, 201)

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


class EventViewTests(BaseTestCase):
    def setUp(self):
        super(EventViewTests, self).setUp()
        self.event = {
            "owners": [
                "http://127.0.0.1:8000/profile/" + str(self.user_bob.pk) + "/"
            ],
            "htags": [
                "foot"
            ],
            "location": {
                "latitude": -0.0030899047836627073,
                "longitude": -0.0017166137695312517
            },
            "title": "Salut",
            "description": "Yo",
            "type": "Rapta",
            "time_start": "2018-05-16T16:45:32.466000+02:00",
            "time_end": "2018-05-16T16:45:32.466022+02:00",
            "is_rapta": True,
            "seats": 1,
            "radius": 1.0,
            "min_age": 18,
            "max_age": 60,
            "is_free": True,
            "is_public": True,
            "members": [
                "http://127.0.0.1:8000/profile/" + str(self.user_bob.pk) + "/"
            ]
        }

    def test_create_event(self):
        url = reverse("event-list")

        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.post(url, self.event, format='json')
        req = self.factory.post(url, self.event, format='json')
        self.assertResponse201(response)
        event = Event.objects.get(title="Salut", description="Yo", type="Rapta")
        serializer = EventSerializer(event, many=False, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()
            # TODO Duplicate test

    def test_list_bob_event(self):
        url = reverse("event-list")

        self.client.force_authenticate(self.user_bob)
        response = self.client.post(url, self.event, format='json')
        self.assertResponse201(response)
        self.client.force_authenticate()

        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        req = self.factory.get(url)
        self.assertResponse200(response)
        event = Event.objects.filter(owners__owner=self.user_bob)
        serializer = EventSerializer(event, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_detail_event(self):
        url = reverse("event-list")

        self.client.force_authenticate(self.user_bob)
        response = self.client.post(url, self.event, format='json')
        self.assertResponse201(response)
        self.client.force_authenticate()

        url = reverse_querystring("event-detail", kwargs={'pk': 2})

        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        req = self.factory.get(url)
        self.assertResponse200(response)
        event = Event.objects.get(pk=2)
        serializer = EventSerializer(event, many=False, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()
