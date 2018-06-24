# serializers
from collections import Counter

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import SerializerErrorMessagesMixin


from rest_profile.models import Profile

# Get the UserModel
UserModel = get_user_model()


class ProfileSerializer(SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    img = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = "__all__"


class UserDetailsSerializer(SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('email',)
