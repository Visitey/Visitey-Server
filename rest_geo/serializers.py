# serializers

from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import SerializerErrorMessagesMixin
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from rest_geo.models import PointOfInterest, Route


class PointOfInterestSerializer(TaggitSerializer, SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    img = Base64ImageField(required=False)
    id = serializers.ReadOnlyField()
    htags = TagListSerializerField()
    location = PointField(required=False)

    class Meta:
        model = PointOfInterest
        fields = "__all__"


class RouteSerializer(TaggitSerializer, SerializerErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    img = Base64ImageField(required=False)
    htags = TagListSerializerField()
    location = PointField(required=False)
    pois = serializers.HyperlinkedRelatedField(many=True, view_name='pointofinterest-detail',
                                               queryset=PointOfInterest.objects.all())

    class Meta:
        model = Route
        fields = "__all__"
