# Generated by Django 2.0.5 on 2018-05-11 14:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(max_length=40, null=True, srid=4326)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('type', models.CharField(default='Rapta', max_length=100)),
                ('timeStart', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start_date')),
                ('timeEnd', models.DateTimeField(default=django.utils.timezone.now, verbose_name='end_date')),
                ('isRapta', models.BooleanField(default=True)),
                ('seats', models.IntegerField(default=1)),
                ('radius', models.FloatField(default=1)),
                ('minAge', models.IntegerField(default=18)),
                ('maxAge', models.IntegerField(default=60)),
                ('isFree', models.BooleanField(default=True)),
                ('isPublic', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('timeStart',),
            },
        ),
    ]
