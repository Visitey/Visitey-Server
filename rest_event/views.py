from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import Distance
from django.utils import timezone
from rest_framework import viewsets

from rest_event.models import Event
from rest_event.serializers import EventSerializer


# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """

        #TODO DOCSTRING QUERYPARAM

        radius = self.request.query_params.get('radius', None)
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        recent_log = self.request.query_params.get('connected', None)
        inprogress = self.request.query_params.get('inprogress', None)
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        day = self.request.query_params.get('day', None)
        hour = self.request.query_params.get('hour', None)
        minmembers = self.request.query_params.get('minmembers', None)
        if radius is not None and lng is not None and lat is not None:
            user_location = fromstr("POINT(%s %s)" % (lng, lat))
            now = timezone.now()
            events = Event.objects.filter(location__distance_lte=(user_location, Distance(km=radius)))
            if year is not None:
                events = events.filter(timeStart__year=year)
                if month is not None:
                    events = events.filter(timeStart__month=month)
                    if day is not None:
                        events = events.filter(timeStart__day=day)
                        if hour is not None:
                            events = events.filter(timeStart__hour=hour)
            if recent_log is not None:
                events = events.filter(owners__owner__last_login__range=(now - timezone.timedelta(minutes=30), now))
            if inprogress is not None:
                events = events.filter(timeStart__lt=now, timeEnd__gt=now)
            # minmembers
            # mindurationleft
            return events
        else:
            return Event.objects.filter(owners__owner=self.request.user)
