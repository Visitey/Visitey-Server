from django.contrib.gis import admin

from .models import Route, PointOfInterest


# Register your models here.

# subclass the GeoModelAdmin to use the locally hosted OpenLayers library
class OlGeoModelAdmin(admin.GeoModelAdmin):
    openlayers_url = 'OpenLayers.js'


# subclass the OSMGeoAdmin to use the locally hosted OpenLayers library
class OlOSMGeoAdmin(admin.OSMGeoAdmin):
    openlayers_url = 'OpenLayers.js'


# register an admin tool for the Location model
# admin.site.register(Location, olGeoModelAdmin)
# the OSMGeoAdmin tool uses the openstreetmap data for a nicer experience
admin.site.register(Route)
admin.site.register(PointOfInterest, admin.OSMGeoAdmin)
