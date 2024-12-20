# Generated by Django 5.0.2 on 2024-06-14 21:12

import django.db.models.deletion
import videomanager.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=40)),
                ('last_checked', models.DateTimeField()),
                ('monitored', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(storage=videomanager.storage.ExistingFileStorage(), upload_to='')),
                ('banner_image', models.ImageField(storage=videomanager.storage.ExistingFileStorage(), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('youtube', 'YouTube')], default='youtube', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=110)),
                ('description', models.TextField()),
                ('upload_date', models.DateField()),
                ('last_checked', models.DateTimeField()),
                ('monitored', models.BooleanField(default=False)),
                ('file', models.FileField(storage=videomanager.storage.ExistingFileStorage(), upload_to='')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videomanager.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_id', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=100)),
                ('last_checked', models.DateTimeField()),
                ('monitored', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videomanager.channel')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='videomanager.playlistsource')),
                ('videos', models.ManyToManyField(related_name='playlists', to='videomanager.video')),
            ],
        ),
    ]
