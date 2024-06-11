import datetime

from django.conf import settings
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


# For planned alternative sources than youtube, such as user created playlist
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
    filename = models.CharField(max_length=110)
    description = models.TextField()
    upload_date = models.DateField()
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# https://stackoverflow.com/questions/3501588/how-to-assign-a-local-file-to-the-filefield-in-django
# If you don't want to open the file, you can also move the file to the media folder and directly set myfile.name ' \
#           'with the relative path to MEDIA_ROOT :
#
# import os
# os.rename('mytest.pdf', '/media/files/mytest.pdf')
# pdfImage = FileSaver()
# pdfImage.myfile.name = '/files/mytest.pdf'
# pdfImage.save()
