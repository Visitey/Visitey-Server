# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from rest_htags.models import Htag


class Profile(models.Model):
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    pseudo = models.CharField(max_length=100, default='', blank=True)
    img = models.ImageField(max_length=None, null=True, blank=True)
    desc = models.TextField(max_length=100, default='', blank=True)
    gender = models.CharField(max_length=100, default='male', blank=True)
    birthdate = models.DateTimeField('birthdate', default=timezone.now)
    phone_number = models.CharField(max_length=100, default='', blank=True)
    relationship = models.CharField(max_length=100, default='', blank=True)
    rank = models.IntegerField(default=0)
    blacklist = models.ManyToManyField('self', default=None)

    # joinMe
    # music
    def __str__(self):
        return self.owner.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
