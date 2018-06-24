# Create your views here.
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import Distance
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_geo.models import PointOfInterest, Route
from rest_geo.serializers import PointOfInterestSerializer, RouteSerializer


class PointOfInterestViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.

      parameters:
        - name: radius
        in: query
        type: integer
        required: true
        description: Search radius in km

        - name: lng
        in: query
        type: float
        required: true
        description: Origin point longitude

        - name: lat
        in: query
        type: float
        required: true
        description: Origin point latitude

    """

    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    # permission_classes

    def get_queryset(self):
        radius = self.request.query_params.get('radius', None)
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        if radius and lng and lat:
            user_location = fromstr("POINT(%s %s)" % (lng, lat))
            pois = PointOfInterest.objects.filter(location__distance_lte=(user_location, Distance(km=radius)))
            return pois
        else:
            return None


class RouteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.

      parameters:
        - name: radius
        in: query
        type: integer
        required: true
        description: Search radius in km

        - name: lng
        in: query
        type: float
        required: true
        description: Origin point longitude

        - name: lat
        in: query
        type: float
        required: true
        description: Origin point latitude

    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    # permission_classes

    def get_queryset(self):
        radius = self.request.query_params.get('radius', None)
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        if radius and lng and lat:
            user_location = fromstr("POINT(%s %s)" % (lng, lat))
            routes = Route.objects.filter(points__location=(user_location, Distance(km=radius)))
            return routes
        else:
            return None
