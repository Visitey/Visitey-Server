from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from rest_htags.models import Htags
from rest_profile.models import Profile


# Create your models here.

class Event(models.Model):
    """ Model to represent Events """
    owners = models.ManyToManyField(Profile, related_name='myevents')
    members = models.ManyToManyField(Profile, related_name='events')
    location = models.PointField(max_length=40, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=100, blank=False, default="Rapta")
    time_start = models.DateTimeField('start_date', auto_now_add=True)
    time_end = models.DateTimeField('end_date', auto_now_add=True)
    htags = TaggableManager(blank=False, through=Htags)
    is_rapta = models.BooleanField(default=True)
    seats = models.IntegerField(default=1)
    radius = models.FloatField(default=1)
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=60)
    # pictures = ArrayField(models.ImageField(null=True, blank=True, upload_to="media", max_length=None), null=True,
    # blank=True) Permissions (les protections)
    is_free = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    # outside / inside place
    # lock / unlock join
    # objects = EventManager()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        unique_together = (("location", "title", "description", "type", "is_rapta", "time_start"),)
        ordering = ('time_start',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure that owners are members
        super(Event, self).save(*args, **kwargs)


def event_changed(sender, **kwargs):
    if kwargs['instance'].members.count() > kwargs['instance'].seats:
        raise ValidationError("You can't assign more than" + str(kwargs['instance'].seats) + " seats")


m2m_changed.connect(event_changed, sender=Event.members.through)
