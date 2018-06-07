# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse


class Profile(models.Model):
    """ Profile model representation """
    # gender_regex = RegexValidator(regex=r'^male$|^female$', message="Gender must be 'male' or 'female'")
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format:
    # '+999999999'. Up to 15 digits " "allowed.") relationship_regex = RegexValidator(regex=r"^single$|^in a
    # relationship$|^engaged$|^married$|^it's " r"complicated$|^in an open "
    # r"relationship$|^widowed$|^separated$|^divorced$|^in a civil union$", message="Relationship must be : 'Single',
    #  'In a Relationship', 'Engaged', " "'Married', 'It's Complicated', 'In an Open Relationship', 'Widowed',
    # " "'Separated', 'Divorced', 'In a Civil Union,'")

    owner = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    pseudo = models.CharField(max_length=15, default='', blank=True)
    img = models.ImageField(max_length=None, null=True, blank=True)
    desc = models.TextField(max_length=100, default='', blank=True)
    gender = models.CharField(max_length=6, default='')
    birthdate = models.DateTimeField('birthdate', default=timezone.now)
    phone_number = models.CharField(max_length=17, default='', blank=True)
    relationship = models.CharField(max_length=40, default='', blank=True)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return self.pseudo + ' - ' + self.owner.username

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('birthdate',)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
