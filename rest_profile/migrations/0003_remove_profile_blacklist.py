# Generated by Django 2.0.5 on 2018-05-11 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_profile', '0002_auto_20180511_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blacklist',
        ),
    ]
