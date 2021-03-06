# Generated by Django 2.0.6 on 2018-06-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rest_profile', '0004_auto_20180605_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('birthdate',), 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=17, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(blank=True, default='', max_length=15, unique=True),
        ),
    ]
