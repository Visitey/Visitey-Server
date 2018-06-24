from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import RequestFactory
from django.utils.http import urlencode
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from rest_friendship.models import Friend, Follow
from rest_friendship.serializers import FriendshipSerializer, FriendshipRequestSerializer, FollowSerializer


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    """Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search', 'Bob'})
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


class BaseTestCase(APITestCase):

    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.user_steve = self.create_user('steve', 'steve@steve.com', self.user_pw)
        self.user_susan = self.create_user('susan', 'susan@susan.com', self.user_pw)
        self.user_amy = self.create_user('amy', 'amy@amy.amy.com', self.user_pw)
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

    def assertResponse405(self, response):
        self.assertEqual(response.status_code, 405)


class FriendshipViewTests(BaseTestCase):

    def setUp(self):
        super(FriendshipViewTests, self).setUp()
        self.friendship_request = Friend.objects.add_friend(self.user_steve.profile, self.user_bob.profile)
        self.follow_request = Follow.objects.add_follower(self.user_bob.profile, self.user_amy.profile)

    def test_friendship_view_friends(self):
        url = reverse('friend-list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        friends = Friend.objects.friends(self.user_bob.profile)
        serializer = FriendshipSerializer(friends, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertResponse200(response)
        self.client.force_authenticate()

    def test_friendship_add_friend(self):
        url = reverse_querystring('friend-add-friend', query_kwargs={'username': self.user_amy.username})

        # test that the view requires authentication to access it

        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST send a friendship request to `username` in query params
        response = self.client.post(url)
        req = self.factory.post(url)
        requests = Friend.objects.sent_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertResponse202(response)
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

        url = reverse('friendshiprequest-list')
        self.client.force_authenticate(self.user_amy)
        # the `username` receive a friend request
        response = self.client.get(url)
        req = self.factory.post(url)
        requests = Friend.objects.unrejected_requests(self.user_amy.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertResponse200(response)
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

        # test if username doesn't exist
        url = reverse_querystring('friend-add-friend', query_kwargs={'username': 'tartantpion'})

        self.client.force_authenticate(self.user_bob)
        # on POST send a friendship request to `username` in query params
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()

    def test_friendship_add_friend_dupe(self):
        url = reverse_querystring('friend-add-friend', query_kwargs={'username': self.user_amy.username})

        # test that the view requires authentication to access it

        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST send a friendship request to `username` in query params
        response = self.client.post(url)
        req = self.factory.post(url)
        requests = Friend.objects.sent_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertResponse202(response)
        self.assertEqual(response.data, serializer.data)

        response = self.client.post(url)
        self.assertResponse400(response)
        self.assertEqual(response.data, {'code': 5001, 'message': 'Friendship request already exist'})
        self.client.force_authenticate()

        url = reverse('friendshiprequest-list')
        self.client.force_authenticate(self.user_amy)
        # the `username` receive a friend request
        response = self.client.get(url)
        req = self.factory.post(url)
        requests = Friend.objects.unrejected_requests(self.user_amy.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_requests(self):
        url = reverse('friendshiprequest-list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.unrejected_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_requests_sent(self):
        url = reverse_querystring('friendshiprequest-list', query_kwargs={'sent': 'true'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.sent_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_requests_rejected(self):
        url = reverse_querystring('friendshiprequest-list', query_kwargs={'rejected': 'true'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.rejected_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_accept(self):
        url = reverse_querystring('friendshiprequest-accept-request',
                                  query_kwargs={'request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_steve)
        # on POST try to accept the friendship request
        # but I am logged in as Steve, so I cannot accept
        # a request sent to Bob
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()

        self.client.force_authenticate(self.user_bob)
        # on POST accept the friendship request
        # and delete it

        response = self.client.post(url)
        self.assertResponse202(response)
        self.assertEqual(response.data, {'message': 'Request accepted'})

        # Test if request is well deleted
        url = reverse_querystring('friendshiprequest-list')
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.unrejected_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_reject(self):
        url = reverse_querystring('friendshiprequest-reject-request',
                                  query_kwargs={'request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_steve)
        # on POST try to reject the friendship request
        # but I am logged in as Steve, so I cannot reject
        # a request sent to Bob
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()

        self.client.force_authenticate(self.user_bob)
        # on POST reject the friendship request
        # and add it to rejected requests
        response = self.client.post(url)
        self.assertResponse202(response)
        self.assertEqual(response.data, {'message': 'Request rejected'})

        # Test if request is well rejected
        url = reverse_querystring('friendshiprequest-list', query_kwargs={'rejected': 'true'})
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.rejected_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_friendship_cancel(self):
        url = reverse_querystring('friendshiprequest-cancel-request',
                                  query_kwargs={'request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST try to cancel the friendship request
        # but I am logged in as Bob, so I cannot cancel
        # a request made by Steve
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()

        self.client.force_authenticate(self.user_steve)
        # on POST cancel the friendship request
        response = self.client.post(url)
        self.assertResponse202(response)
        self.assertEqual(response.data, {'message': 'Request cancelled'})
        self.client.force_authenticate()

        self.client.force_authenticate(self.user_bob)
        # Check if request is well canceled
        url = reverse_querystring('friendshiprequest-list')
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        requests = Friend.objects.unrejected_requests(self.user_bob.profile)
        serializer = FriendshipRequestSerializer(requests, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate()

    def test_followers_list(self):
        url = reverse_querystring('follow-list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        response = self.client.get(url)
        followers = Follow.objects.followers(self.user_bob.profile)
        serializer = FollowSerializer(followers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertResponse200(response)
        self.client.force_authenticate()

    def test_following_list(self):
        url = reverse_querystring('follow-list', query_kwargs={'following': 'true'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST
        response = self.client.get(url)
        req = self.factory.get(url)
        follows = Follow.objects.filter(follower=self.user_bob.profile).all()
        serializer = FollowSerializer(follows, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)
        self.assertResponse200(response)
        self.client.force_authenticate()

    def test_follower_add(self):
        url = reverse_querystring('follow-add-follow', query_kwargs={'username': self.user_susan.username})

        # test that the view requires authentication to access it
        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST follow user `username`
        response = self.client.post(url)
        self.assertResponse202(response)
        self.assertEqual(response.data, {'message': 'Follower added'})

        url = reverse_querystring('follow-list', query_kwargs={'following': 'true'})
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        follows = Follow.objects.filter(follower=self.user_bob.profile).all()
        serializer = FollowSerializer(follows, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)

        url = reverse_querystring('follow-add-follow', query_kwargs={'username': self.user_susan.username})
        response = self.client.post(url)
        self.assertResponse400(response)
        self.assertEqual(response.data, {'code': '6001', 'message': 'Follow already exist'})

        url = reverse_querystring('follow-add-follow', query_kwargs={'username': 'tartanpion'})
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()

    def test_follower_remove(self):
        url = reverse_querystring('follow-remove-follow', query_kwargs={'username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.post(url)
        self.assertResponse401(response)

        self.client.force_authenticate(self.user_bob)
        # on POST
        response = self.client.post(url)
        self.assertResponse202(response)
        self.assertEqual(response.data, {'message': 'Follower removed'})

        url = reverse_querystring('follow-list', query_kwargs={'following': 'true'})
        response = self.client.get(url)
        self.assertResponse200(response)
        req = self.factory.get(url)
        follows = Follow.objects.filter(follower=self.user_bob.profile).all()
        serializer = FollowSerializer(follows, many=True, context={'request': req})
        self.assertEqual(response.data, serializer.data)

        url = reverse_querystring('follow-remove-follow', query_kwargs={'username': self.user_amy.username})
        response = self.client.post(url)
        self.assertResponse400(response)
        self.assertEqual(response.data, {'code': 6002, 'message': 'Follower doesn\'t exist'})

        url = reverse_querystring('follow-remove-follow', query_kwargs={'username': 'tartanpion'})
        response = self.client.post(url)
        self.assertResponse404(response)
        self.client.force_authenticate()
