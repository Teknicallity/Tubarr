import datetime
import os.path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from .storage import ExistingFileStorage
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

class Channel(models.Model):
    channel_id = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)
    profile_image = models.ImageField(storage=ExistingFileStorage())
    banner_image = models.ImageField(storage=ExistingFileStorage())

    def save(self, *args, **kwargs):
        self.profile_image.name = f'{self.channel_id}/avatar.jpg'
        self.banner_image.name = f'{self.channel_id}/banner.jpg'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# For planned alternative sources than youtube, such as user created playlist
class PlaylistSource(models.Model):
    SOURCE_YOUTUBE = 'youtube'
    SOURCE_CHOICES = [
        (SOURCE_YOUTUBE, 'YouTube'),
    ]

    name = models.CharField(max_length=20, choices=SOURCE_CHOICES, blank=False, default=SOURCE_YOUTUBE)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    playlist_id = models.CharField(max_length=40)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_checked = models.DateTimeField()
    monitored = models.BooleanField(default=False)
    videos = models.ManyToManyField('Video', related_name='playlists')
    source = models.ForeignKey(PlaylistSource, on_delete=models.PROTECT)

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
    file = models.FileField(storage=ExistingFileStorage())

    def save(self, *args, **kwargs):
        # Set the video_file path using the channel_id and video_name
        self.file.name = f'{self.channel.channel_id}/{self.filename}'
        super().save(*args, **kwargs)

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
