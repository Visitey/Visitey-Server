from rest_framework import serializers
from rest_framework_friendly_errors.mixins import SerializerErrorMessagesMixin

from rest_friendship.models import Friend, FriendshipRequest, Follow
from rest_profile.models import Profile


class FriendshipSerializer(SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    to_user = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                  queryset=Profile.objects.all())
    from_user = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                    queryset=Profile.objects.all())
    id = serializers.ReadOnlyField()

    class Meta:
        model = Friend
        fields = "__all__"


class FriendshipRequestSerializer(SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    to_user = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                  queryset=Profile.objects.all())
    from_user = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                    queryset=Profile.objects.all())
    id = serializers.ReadOnlyField()

    class Meta:
        model = FriendshipRequest
        fields = "__all__"


class FollowSerializer(SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    follower = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                   queryset=Profile.objects.all())
    followee = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail',
                                                   queryset=Profile.objects.all())
    id = serializers.ReadOnlyField()

    class Meta:
        model = Follow
        fields = "__all__"
