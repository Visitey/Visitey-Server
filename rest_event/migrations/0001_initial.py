# Generated by Django 2.0.5 on 2018-05-20 16:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models


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
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(default='Rapta', max_length=100)),
                ('time_start', models.DateTimeField(auto_now_add=True, verbose_name='start_date')),
                ('time_end', models.DateTimeField(auto_now_add=True, verbose_name='end_date')),
                ('is_rapta', models.BooleanField(default=True)),
                ('seats', models.IntegerField(default=1)),
                ('radius', models.FloatField(default=1)),
                ('min_age', models.IntegerField(default=18)),
                ('max_age', models.IntegerField(default=60)),
                ('is_free', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ('time_start',),
            },
        ),
    ]
