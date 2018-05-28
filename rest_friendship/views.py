from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_friendship.exceptions import AlreadyExistsError
from rest_friendship.models import Friend, Follow
from rest_friendship.serializers import FriendshipSerializer, FriendshipRequestSerializer, FollowSerializer
from rest_profile.models import Profile

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')


class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
        """
    serializer_class = FriendshipRequestSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """
        rejected = self.request.query_params.get('rejected', None)
        sent = self.request.query_params.get('sent', None)
        owner = Profile.objects.get(owner=self.request.user)
        if rejected is not None:
            return Friend.objects.rejected_requests(owner)
        if sent is not None:
            return Friend.objects.sent_requests(owner)
        return Friend.objects.unread_requests(owner)

    @action(methods=['post'], detail=False, url_name='accept-request', url_path='accept_request')
    def friendship_accept(self, arg):
        """ Accept a friendship request """
        friendship_request_id = int(self.request.query_params.get('request_id', None))
        if friendship_request_id is not None:
            request = get_object_or_404(Profile, owner=self.request.user)
            try:
                request = request.friendship_requests_received.get(id=friendship_request_id)
            except ObjectDoesNotExist as e:
                raise NotFound('request id : ' + str(friendship_request_id) + ' does not exist !')
            else:
                request.accept()
            content = {'message': 'Request accepted'}
            return Response(content, status=status.HTTP_202_ACCEPTED)
        serializer = FriendshipRequestSerializer(Friend.objects.unrejected_requests(self.request.user.profile),
                                                 many=True, context={'request': self.request})
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_name='reject-request', url_path='reject_request')
    def friendship_reject(self, arg):
        """ Reject a friendship request """
        friendship_request_id = int(self.request.query_params.get('request_id', None))
        if friendship_request_id is not None:
            request = get_object_or_404(Profile, owner=self.request.user)
            try:
                request = request.friendship_requests_received.get(id=friendship_request_id)
            except ObjectDoesNotExist as e:
                raise NotFound('request id : ' + str(friendship_request_id) + ' does not exist !')
            else:
                request.reject()
            content = {'message': 'Request rejected'}
            return Response(content, status=status.HTTP_202_ACCEPTED)
        serializer = FriendshipRequestSerializer(Friend.objects.rejected_requests(self.request.user.profile),
                                                 many=True, context={'request': self.request})
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_name='cancel-request', url_path='cancel_request')
    def friendship_cancel(self, arg):
        """ Cancel a friendship request """
        friendship_request_id = int(self.request.query_params.get('request_id', None))
        if friendship_request_id is not None:
            request = get_object_or_404(Profile, owner=self.request.user)
            try:
                request = request.friendship_requests_sent.get(id=friendship_request_id)
            except ObjectDoesNotExist as e:
                raise NotFound('request id : ' + str(friendship_request_id) + ' does not exist !')
            else:
                request.cancel()
                content = {'message': 'Request cancelled'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


class FriendshipViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """
        return Friend.objects.select_related('from_user', 'to_user').filter(to_user=self.request.user.profile).all()

    @action(methods=['post'], detail=False, url_name='add-friend', url_path='add_friend')
    def friendship_add_friend(self, arg):
        """ Create a FriendshipRequest """
        to_username = self.request.query_params.get('username', None)
        from_user = get_object_or_404(Profile, owner=self.request.user)
        if to_username is not None:
            try:
                to_user = Profile.objects.get(owner__username=to_username)
            except ObjectDoesNotExist as e:
                raise NotFound(to_username + ' does not exist !')
            else:
                try:
                    Friend.objects.add_friend(from_user, to_user)
                except AlreadyExistsError as e:
                    content = {'code': 5001, 'message': 'Friendship request already exist'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = FriendshipRequestSerializer(Friend.objects.sent_requests(from_user),
                                                             many=True, context={'request': self.request})
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
        """
    serializer_class = FollowSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """

        following = self.request.query_params.get('following', None)
        if following is not None:
            return Follow.objects.filter(follower=self.request.user.profile).all()
        else:
            return Follow.objects.filter(followee=self.request.user.profile).all()

    @action(methods=['post'], detail=False, url_name='add-follow', url_path='add_follow')
    def follower_add(self, arg):
        """ Create a following relationship """
        to_username = self.request.query_params.get('username', None)
        follower = get_object_or_404(Profile, owner=self.request.user)
        if to_username is not None:
            try:
                followee = Profile.objects.get(owner__username=to_username)
            except ObjectDoesNotExist as e:
                raise NotFound(to_username + ' does not exist !')
            else:
                try:
                    Follow.objects.add_follower(follower, followee)
                except AlreadyExistsError as e:
                    content = {'code': '6001', 'message': 'Follow already exist'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    content = {'message': 'Follower added'}
                    return Response(content, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_name='remove-follow', url_path='remove_follow')
    def follower_remove(self, arg):
        """ Remove a following relationship """
        to_username = self.request.query_params.get('username', None)
        follower = get_object_or_404(Profile, owner=self.request.user)
        if to_username is not None:
            try:
                followee = Profile.objects.get(owner__username=to_username)
            except ObjectDoesNotExist as e:
                raise NotFound(to_username + ' does not exist !')
            else:
                if Follow.objects.remove_follower(follower, followee):
                    content = {'message': 'Follower removed'}
                    return Response(content, status=status.HTTP_202_ACCEPTED)
                else:
                    content = {'code': 6002, 'message': 'Follower doesn\'t exist'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
