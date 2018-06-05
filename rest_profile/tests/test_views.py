from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import RequestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_profile.models import Profile
from rest_profile.serializers import ProfileSerializer


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


class ProfileViewTests(BaseTestCase):

    def setUp(self):
        super(ProfileViewTests, self).setUp()

    def test_get_profile(self):
        url = reverse('profile-list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        req = self.factory.get(url)
        profile = Profile.objects.filter(id=self.user_bob.profile.id)
        serializer = ProfileSerializer(profile,many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.assertResponse200(response)
        self.client.force_authenticate()

    def test_update_profile(self):
        put_profile = {
            "myevents": [],
            "events": [],
            "pseudo": "trololo",
            "desc": "Kappa",
            "gender": "Male",
            "birthdate": "2018-06-01T14:01:37Z",
            "phone_number": "0783316398",
            "relationship": "binary",
            "rank": -1,
        }

        url = reverse('profile-detail', kwargs={'pk': self.user_bob.profile.id})

        # test that the view requires authentication to access it
        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.put(url, put_profile)
        req = self.factory.put(url)
        profile = Profile.objects.get(id=self.user_bob.profile.id)
        serializer = ProfileSerializer(profile, context={'request': req})
        print(response.data)
        self.assertEqual(response.data, serializer.data)
        self.assertResponse200(response)
        self.client.force_authenticate()

    # TODO VALIDATORS Gender, phone number etc...
