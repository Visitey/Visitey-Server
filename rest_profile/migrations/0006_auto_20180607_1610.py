# Generated by Django 2.0.6 on 2018-06-07 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rest_profile', '0005_auto_20180606_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=17),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]