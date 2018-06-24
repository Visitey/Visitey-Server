# Generated by Django 2.0.6 on 2018-06-20 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rest_profile', '0007_auto_20180620_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='', max_length=6, validators=[
                django.core.validators.RegexValidator(message="Gender must be 'male' or 'female'",
                                                      regex='^male$|^female$|^Male$|^Female$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=17, validators=[
                django.core.validators.RegexValidator(
                    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                    regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='relationship',
            field=models.CharField(blank=True, default='', max_length=40, validators=[
                django.core.validators.RegexValidator(
                    message="Relationship must be : 'Single','In a Relationship', 'Engaged', 'Married', 'It's Complicated', 'In an Open Relationship', 'Widowed', 'Separated', 'Divorced', 'In a Civil Union,'",
                    regex="^single$|^in a relationship$|^engaged$|^married$|^it's complicated$|^in an open relationship$|^widowed$|^separated$|^divorced$|^in a civil union$")]),
        ),
    ]
