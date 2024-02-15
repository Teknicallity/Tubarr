import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class Channel(models.Model):
    channel_id = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)
    profile_pic_path = models.FilePathField()

    def __str__(self):
        return self.name


class PlaylistSource(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    playlist_id = models.CharField(max_length=40)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)
    videos = models.ManyToManyField('Video', related_name='playlists')
    source = models.ForeignKey(PlaylistSource, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Video(models.Model):
    video_id = models.CharField(max_length=15)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file_path = models.FilePathField()
    description = models.CharField(max_length=5000)
    upload_date = models.DateTimeField()
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)

    def __str__(self):
        return self.title
