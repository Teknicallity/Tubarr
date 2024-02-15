# Generated by Django 5.0.1 on 2024-02-13 15:01

import django.db.models.deletion
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
                ('channelID', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=40)),
                ('last_checked', models.DateTimeField()),
                ('monitored', models.BooleanField(default=False)),
                ('profile_pic_path', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=100)),
                ('file_path', models.FilePathField()),
                ('description', models.CharField(max_length=5000)),
                ('upload_date', models.DateTimeField()),
                ('last_checked', models.DateTimeField()),
                ('monitored', models.BooleanField(default=False)),
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
                ('videos', models.ManyToManyField(related_name='playlists', to='videomanager.video')),
            ],
        ),
    ]
