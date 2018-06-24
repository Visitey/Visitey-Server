from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import RequestFactory
from rest_framework.test import APIClient, APITestCase

from rest_friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from rest_friendship.models import Friend, FriendshipRequest, Follow


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


class FriendshipModelTests(BaseTestCase):

    def test_friendshiprequest_name(self):
        friendrequest = FriendshipRequest.objects.create(from_user=self.user_bob.profile,
                                                         to_user=self.user_steve.profile)
        expected_object_name = "User #%s friendship requested #%s" % (self.user_bob.profile.id,
                                                                      self.user_steve.profile.id)
        self.assertEquals(expected_object_name, str(friendrequest))

    def test_friend_name(self):
        friend = Friend.objects.create(from_user=self.user_bob.profile,
                                       to_user=self.user_steve.profile)
        expected_object_name = "User #%s is friends with #%s" % (self.user_steve.profile.id,
                                                                 self.user_bob.profile.id)
        self.assertEquals(expected_object_name, str(friend))

    def test_follow_name(self):
        follow = Follow.objects.create(follower=self.user_bob.profile,
                                       followee=self.user_steve.profile)
        expected_object_name = "User #%s follows #%s" % (self.user_bob.profile.id,
                                                         self.user_steve.profile.id)
        self.assertEquals(expected_object_name, str(follow))

    def test_friendship_request(self):
        # Bob wants to be friends with Steve
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
        self.assertFalse(Friend.objects.remove_friend(self.user_bob.profile, self.user_bob.profile))

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
        # Bob wants to be friends with Steve
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
