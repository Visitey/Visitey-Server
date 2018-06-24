from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from rest_framework.reverse import reverse
from taggit.managers import TaggableManager

from rest_htags.models import Htags


class PointOfInterest(models.Model):
    """ Model to represent POIs"""

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True, null=True)
    location = models.PointField()
    img = models.ImageField(max_length=None, null=True, blank=True)
    htags = TaggableManager(blank=True, through=Htags)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pointofinterest-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('PointOfInterest')
        verbose_name_plural = _('PointOfInterest')
        ordering = ('title',)


class Route(models.Model):
    """ Model to represent Routes """

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True, null=True)
    img = models.ImageField(max_length=None, null=True, blank=True)
    points = models.ManyToManyField(PointOfInterest, related_name='routes')
    htags = TaggableManager(blank=True, through=Htags)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('route-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')
        ordering = ('title',)
