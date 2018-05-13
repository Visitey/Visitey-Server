# Generated by Django 2.0.5 on 2018-05-11 14:13

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rest_htags', '0001_initial'),
        ('rest_event', '0001_initial'),
        ('rest_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='htags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='rest_htags.Htags', to='rest_htags.Htag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(related_name='events', to='rest_profile.Profile'),
        ),
        migrations.AddField(
            model_name='event',
            name='owners',
            field=models.ManyToManyField(related_name='myevents', to='rest_profile.Profile'),
        ),
    ]
