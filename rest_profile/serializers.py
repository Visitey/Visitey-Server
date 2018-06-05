# serializers
from collections import Counter

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from rest_event.models import Event
from rest_profile.models import Profile

# Get the UserModel
UserModel = get_user_model()


class ProfileSerializer(FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    myevents = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail', queryset=Event.objects.all())
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail', queryset=Event.objects.all())
    best_htags = serializers.SerializerMethodField()
    img = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    @staticmethod
    def get_best_htags(obj):
        c = Counter(obj.myevents.values_list('htags__name', flat=True))
        c.most_common(5)
        c = +c
        return c.keys()


class UserDetailsSerializer(FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('email',)
