from django.contrib import admin

# Register your models here.
from rest_chat import models

admin.site.register(models.Message)
admin.site.register(models.Thread)
admin.site.register(models.Participant)
