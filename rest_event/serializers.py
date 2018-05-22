# serializers
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from rest_event.models import Event
from rest_profile.models import Profile


class EventSerializer(TaggitSerializer, FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    owners = serializers.HyperlinkedRelatedField(many=True, view_name='profile-detail', queryset=Profile.objects.all())
    id = serializers.ReadOnlyField()
    htags = TagListSerializerField()
    location = PointField(required=False)

    class Meta:
        model = Event
        fields = "__all__"

    validators = [
        UniqueTogetherValidator(
            queryset=Event.objects.all(),
            fields=('location', 'title', 'description', 'type', 'is_rapta', 'time_start'),
            message="UniqueTogetherError"
        )
    ]
