# Generated by Django 2.0.6 on 2018-06-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_profile', '0003_auto_20180605_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=17),
        ),
    ]