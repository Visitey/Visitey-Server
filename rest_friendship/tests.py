from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, RequestFactory
from django.utils.http import urlencode
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from rest_friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from rest_friendship.models import Friend, Follow, FriendshipRequest
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


class BaseTestCase(TestCase):

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

    def login(self, user, password):
        return login(self, user, password)

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


class FriendshipModelTests(BaseTestCase):

    def test_friendship_request(self):
        ### Bob wants to be friends with Steve
        req1 = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile)

        # Ensure neither have friends already
        self.assertEqual(Friend.objects.friends(self.user_bob.profile), [])
        self.assertEqual(Friend.objects.friends(self.user_steve.profile), [])

        # Ensure FriendshipRequest is created
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob.profile).count(), 1)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve.profile).count(), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve.profile), 1)

        # Ensure the proper sides have requests or not
        self.assertEqual(len(Friend.objects.requests(self.user_bob.profile)), 0)
        self.assertEqual(len(Friend.objects.requests(self.user_steve.profile)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_bob.profile)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_steve.profile)), 0)

        self.assertEqual(len(Friend.objects.unread_requests(self.user_steve.profile)), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve.profile), 1)

        self.assertEqual(len(Friend.objects.rejected_requests(self.user_steve.profile)), 0)

        self.assertEqual(len(Friend.objects.unrejected_requests(self.user_steve.profile)), 1)
        self.assertEqual(Friend.objects.unrejected_request_count(self.user_steve.profile), 1)

        # Ensure they aren't friends at this point
        self.assertFalse(Friend.objects.are_friends(self.user_bob.profile, self.user_steve.profile))

        # Accept the request
        req1.accept()

        # Ensure neither have pending requests
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob.profile).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve.profile).count(), 0)

        # Ensure both are in each other's friend lists
        self.assertEqual(Friend.objects.friends(self.user_bob.profile), [self.user_steve.profile])
        self.assertEqual(Friend.objects.friends(self.user_steve.profile), [self.user_bob.profile])
        self.assertTrue(Friend.objects.are_friends(self.user_bob.profile, self.user_steve.profile))

        # Make sure we can remove friendship
        self.assertTrue(Friend.objects.remove_friend(self.user_bob.profile, self.user_steve.profile))
        self.assertFalse(Friend.objects.are_friends(self.user_bob.profile, self.user_steve.profile))
        self.assertFalse(Friend.objects.remove_friend(self.user_bob.profile, self.user_steve.profile))

        # Susan wants to be friends with Amy, but cancels it
        req2 = Friend.objects.add_friend(self.user_susan.profile, self.user_amy.profile)
        self.assertEqual(Friend.objects.friends(self.user_susan.profile), [])
        self.assertEqual(Friend.objects.friends(self.user_amy.profile), [])
        req2.cancel()
        self.assertEqual(Friend.objects.requests(self.user_susan.profile), [])
        self.assertEqual(Friend.objects.requests(self.user_amy.profile), [])

        # Susan wants to be friends with Amy, but Amy rejects it
        req3 = Friend.objects.add_friend(self.user_susan.profile, self.user_amy.profile)
        self.assertEqual(Friend.objects.friends(self.user_susan.profile), [])
        self.assertEqual(Friend.objects.friends(self.user_amy.profile), [])
        req3.reject()

        # Duplicated requests raise a more specific subclass of IntegrityError.
        with self.assertRaises(AlreadyExistsError):
            Friend.objects.add_friend(self.user_susan.profile, self.user_amy.profile)

        self.assertFalse(Friend.objects.are_friends(self.user_susan.profile, self.user_amy.profile))
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy.profile)), 1)
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy.profile)), 1)

        # let's try that again..
        req3.delete()

        # Susan wants to be friends with Amy, and Amy reads it
        req4 = Friend.objects.add_friend(self.user_susan.profile, self.user_amy.profile)
        req4.mark_viewed()

        self.assertFalse(Friend.objects.are_friends(self.user_susan.profile, self.user_amy.profile))
        self.assertEqual(len(Friend.objects.read_requests(self.user_amy.profile)), 1)

        # Ensure we can't be friends with ourselves
        with self.assertRaises(ValidationError):
            Friend.objects.add_friend(self.user_bob.profile, self.user_bob.profile)

        # Ensure we can't do it manually either
        with self.assertRaises(ValidationError):
            Friend.objects.create(to_user=self.user_bob.profile, from_user=self.user_bob.profile)

    def test_already_friends_with_request(self):
        # Make Bob and Steve friends
        req = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile)
        req.accept()

        with self.assertRaises(AlreadyFriendsError):
            req2 = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile)

    def test_multiple_friendship_requests(self):
        """ Ensure multiple friendship requests are handled properly """
        ### Bob wants to be friends with Steve
        req1 = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile)

        # Ensure neither have friends already
        self.assertEqual(Friend.objects.friends(self.user_bob.profile), [])
        self.assertEqual(Friend.objects.friends(self.user_steve.profile), [])

        # Ensure FriendshipRequest is created
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob.profile).count(), 1)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve.profile).count(), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve.profile), 1)

        # Steve also wants to be friends with Bob before Bob replies
        req2 = Friend.objects.add_friend(self.user_steve.profile, self.user_bob.profile)

        # Ensure they aren't friends at this point
        self.assertFalse(Friend.objects.are_friends(self.user_bob.profile, self.user_steve.profile))

        # Accept the request
        req1.accept()

        # Ensure neither have pending requests
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob.profile).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve.profile).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_steve.profile).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_bob.profile).count(), 0)

    def test_multiple_calls_add_friend(self):
        """ Ensure multiple calls with same friends, but different message works as expected """
        req1 = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile, message='Testing')

        with self.assertRaises(AlreadyExistsError):
            req2 = Friend.objects.add_friend(self.user_bob.profile, self.user_steve.profile, message='Foo Bar')

    def test_following(self):
        # Bob follows Steve
        req1 = Follow.objects.add_follower(self.user_bob.profile, self.user_steve.profile)
        self.assertEqual(len(Follow.objects.followers(self.user_steve.profile)), 1)
        self.assertEqual(len(Follow.objects.following(self.user_bob.profile)), 1)
        self.assertEqual(Follow.objects.followers(self.user_steve.profile), [self.user_bob.profile])
        self.assertEqual(Follow.objects.following(self.user_bob.profile), [self.user_steve.profile])

        self.assertTrue(Follow.objects.follows(self.user_bob.profile, self.user_steve.profile))
        self.assertFalse(Follow.objects.follows(self.user_steve.profile, self.user_bob.profile))

        # Duplicated requests raise a more specific subclass of IntegrityError.
        with self.assertRaises(IntegrityError):
            Follow.objects.add_follower(self.user_bob.profile, self.user_steve.profile)
        with self.assertRaises(AlreadyExistsError):
            Follow.objects.add_follower(self.user_bob.profile, self.user_steve.profile)

        # Remove the relationship
        self.assertTrue(Follow.objects.remove_follower(self.user_bob.profile, self.user_steve.profile))
        self.assertEqual(len(Follow.objects.followers(self.user_steve.profile)), 0)
        self.assertEqual(len(Follow.objects.following(self.user_bob.profile)), 0)
        self.assertFalse(Follow.objects.follows(self.user_bob.profile, self.user_steve.profile))

        # Ensure we canot follow ourselves
        with self.assertRaises(ValidationError):
            Follow.objects.add_follower(self.user_bob.profile, self.user_bob.profile)

        with self.assertRaises(ValidationError):
            Follow.objects.create(follower=self.user_bob.profile, followee=self.user_bob.profile)


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

    def test_friendship_followers(self):
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

    def test_friendship_following(self):
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
        self.client.force_authenticate()
