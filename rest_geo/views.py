from django.http.multipartparser import MultiPartParser
# Create your views here.
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, FormParser

from rest_geo.models import PointOfInterest, Route
from rest_geo.serializers import PointOfInterestSerializer, RouteSerializer


class PointOfInterestViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.
    """

    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    # permission_classes


class RouteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    # permission_classes
