from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from rest_group.models import Group


class GroupSerializer(FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
