# Generated by Django 2.0.5 on 2018-05-20 16:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rest_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='rest_profile.Profile')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='rest_profile.Profile')),
            ],
            options={
                'verbose_name': 'Following Relationship',
                'verbose_name_plural': 'Following Relationships',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_unused_friend_relation', to='rest_profile.Profile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='rest_profile.Profile')),
            ],
            options={
                'verbose_name': 'Friend',
                'verbose_name_plural': 'Friends',
            },
        ),
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='Message')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('rejected', models.DateTimeField(blank=True, null=True)),
                ('viewed', models.DateTimeField(blank=True, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_sent', to='rest_profile.Profile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_received', to='rest_profile.Profile')),
            ],
            options={
                'verbose_name': 'Friendship Request',
                'verbose_name_plural': 'Friendship Requests',
            },
        ),
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together={('from_user', 'to_user')},
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('from_user', 'to_user')},
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'followee')},
        ),
    ]
