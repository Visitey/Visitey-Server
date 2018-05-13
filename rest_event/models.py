from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.utils.timezone import now
from taggit.managers import TaggableManager

from rest_htags.models import Htags
from rest_profile.models import Profile


# Create your models here.


class Event(models.Model):
    owners = models.ManyToManyField(Profile, related_name='myevents')
    members = models.ManyToManyField(Profile, related_name='events')
    location = models.PointField(max_length=40, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    type = models.CharField(max_length=100, blank=False, default="Rapta")
    timeStart = models.DateTimeField('start_date', default=now)
    timeEnd = models.DateTimeField('end_date', default=now)
    htags = TaggableManager(blank=False, through=Htags)
    isRapta = models.BooleanField(default=True)
    seats = models.IntegerField(default=1)
    radius = models.FloatField(default=1)
    minAge = models.IntegerField(default=18)
    maxAge = models.IntegerField(default=60)
    #pictures = ArrayField(models.ImageField(null=True, blank=True, upload_to="media", max_length=None), null=True, blank=True)
    # Permissions (les protections)
    isFree = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)

    # outside / inside place
    # lock / unlock join
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timeStart',)


def event_changed(sender, **kwargs):
    if kwargs['instance'].members.count() > kwargs['instance'].seats:
        raise ValidationError("You can't assign more than" + str(kwargs['instance'].seats) + " seats")


m2m_changed.connect(event_changed, sender=Event.members.through)
