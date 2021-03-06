# Generated by Django 2.0.6 on 2018-06-06 15:55

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rest_htags', '0001_initial'),
        ('rest_geo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointofinterest',
            options={'ordering': ('title',), 'verbose_name': 'PointOfInterest',
                     'verbose_name_plural': 'PointOfInterest'},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ('title',), 'verbose_name': 'Route', 'verbose_name_plural': 'Routes'},
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='htags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                  through='rest_htags.Htags', to='rest_htags.Htag',
                                                  verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='route',
            name='htags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                  through='rest_htags.Htags', to='rest_htags.Htag',
                                                  verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='route',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='route',
            name='points',
            field=models.ManyToManyField(related_name='routes', to='rest_geo.PointOfInterest'),
        ),
    ]
