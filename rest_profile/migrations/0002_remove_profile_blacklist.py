# Generated by Django 2.0.5 on 2018-06-01 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blacklist',
        ),
    ]
