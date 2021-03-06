# Generated by Django 2.0.6 on 2018-06-20 15:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rest_profile', '0006_auto_20180607_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='', max_length=6, validators=[
                django.core.validators.RegexValidator(message="Gender must be 'male' or 'female'",
                                                      regex='^male$|^female$')]),
        ),
    ]
