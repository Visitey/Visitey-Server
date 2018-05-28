# Create your models here.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import TagBase, GenericTaggedItemBase


class Htag(TagBase):
    name = models.CharField(max_length=100, default='Tag', blank=False)
    popularity = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Htags(GenericTaggedItemBase):
    tag = models.ForeignKey(Htag,
                            related_name="%(app_label)s_%(class)s_items",
                            on_delete=models.CASCADE)
