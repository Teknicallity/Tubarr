import datetime
import os.path
import logging

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from .storage import ExistingFileStorage
from django.utils import timezone
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)


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

    def delete(self, *args, **kwargs):
        logger.info(f'Deleting channel: {self.name}')
        playlists = self.playlist_set.all()
        try:
            for playlist in playlists:
                playlist.delete()
            videos = self.video_set.all()
            for video in videos:
                video.delete()
        except PermissionError as e:
            logger.warning(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise e
        else:
            self.profile_image.close()
            self.profile_image.delete(save=True)
            self.banner_image.close()
            self.banner_image.delete(save=True)
            os.rmdir(os.path.join(settings.MEDIA_ROOT, self.channel_id))
            super(Channel, self).delete(*args, **kwargs)

    def is_empty(self):
        return self.playlist_set.count() == 0 and self.video_set.count() == 0

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

    def delete(self, *args, **kwargs):
        logger.info(f'Deleting playlist: {self.name}')
        video_set = self.videos.all()
        channel = self.channel
        try:
            for video in video_set:
                if video.playlists.count() <= 1 and video.channel.channel_id == channel.channel_id:
                    video.delete()
        except PermissionError as e:
            logger.warning(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise e
        else:
            super(Playlist, self).delete(*args, **kwargs)

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

    def delete(self, *args, **kwargs):
        # temp_video = self
        try:
            logger.debug(f'Deleting video file: {self.file.name}')
            self.file.close()
            self.file.delete(save=True)
        except PermissionError as e:
            logger.warning("Video file could not be deleted. In use by another process")
            raise e
        else:
            line = delete_video_id_from_ytdlp_archive(self.video_id)
            logger.debug(f'downloaded.txt line: {line}')
            channel = self.channel
            try:
                logger.debug(f'Deleting video entry: {self.video_id}')
                super(Video, self).delete(*args, **kwargs)
            except Exception as e:
                logger.warning(e)
                raise e

    def __str__(self):
        return self.title


# https://docs.djangoproject.com/en/5.0/topics/signals/
# @receiver(post_delete, sender=Video)
# def clean_up_deletion(sender, instance, **kwargs):
#     logger.debug(f'Deleting video file {instance.file.name}')
#     instance.file.delete()  # works

# https://stackoverflow.com/questions/3501588/how-to-assign-a-local-file-to-the-filefield-in-django
# If you don't want to open the file, you can also move the file to the media folder and directly set myfile.name ' \
#           'with the relative path to MEDIA_ROOT :
#
# import os
# os.rename('mytest.pdf', '/media/files/mytest.pdf')
# pdfImage = FileSaver()
# pdfImage.myfile.name = '/files/mytest.pdf'
# pdfImage.save()

def delete_video_id_from_ytdlp_archive(video_id):
    actual_line = ''
    line_number = 0
    try:
        with open(os.path.join(settings.CONFIG_DIR, 'ytdlp', 'downloaded.txt'), 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            remaining_lines = []
            for line in lines:
                line_number += 1
                if line.split(' ')[1].strip() != video_id:
                    remaining_lines.append(line)
                else:
                    actual_line = line.strip()
            f.seek(0)
            f.truncate()
            f.writelines(remaining_lines)

    except FileNotFoundError:
        logger.debug("The file was not found.")
    except IOError:
        logger.warning("An I/O error occurred.")
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}")
    else:
        return actual_line
