from django.db import models

# Create your models here.
from rest_profile.models import Profile


class GroupingManager(models.Manager):
    """ Grouping manager """


class Group(models.Model):
    """ Model to represent Groups """
    admin = models.ManyToManyField(Profile, related_name='admin_group')
    members = models.ManyToManyField(Profile, related_name='group')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    objects = GroupingManager()
