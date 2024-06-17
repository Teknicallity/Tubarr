from datetime import datetime
import os.path
import logging

from videomanager.content_handlers.content import Content
from videomanager.models import Channel
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


class Video(Content):
    def __init__(self, url=None, ytdlp_info=None):
        super().__init__()
        self.url = url

        self.video_title = None
        self.video_id = None
        self.video_description = None
        self.video_categories = None
        self.video_tags = None
        self.thumbnail_url = None
        self.upload_date = None

        self.info_dict = ytdlp_info

    def fill_info(self):
        if self.info_dict is None:
            ydl = self._initial_ydl_opts()
            self.info_dict = ydl.extract_info(self.url, download=False)

        self.video_title = self.info_dict['title']
        self.video_id = self.info_dict['id']
        self.video_description = self.info_dict['description']
        self.video_categories = self.info_dict['categories']
        self.video_tags = self.info_dict['tags']
        self.channel_id = self.info_dict['channel_id']
        self.channel_name = self.info_dict['channel']
        self.thumbnail_url = self.info_dict['thumbnail']
        self.upload_date = self.info_dict['upload_date']

    def get_attribute_dict(self) -> dict:
        info = {
            'type': 'video',
            'url': self.url,
            'video_title': self.video_title,
            'video_id': self.video_id,
            'video_description': self.video_description,
            'video_categories': self.video_categories,
            'video_tags': self.video_tags,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'thumbnail_url': self.thumbnail_url,
            'upload_date': self.upload_date,
            'filenames': self.filenames,
            'downloaded': self.downloaded,
        }
        return info

    def download(self):
        self.download_path = os.path.join(settings.MEDIA_ROOT, self.channel_id)

        ydl = self._get_download_opts()
        ydl.download(self.url)

        # return self.download_path, self.filename

    def insert_into_db(self):
        channel_entry, created = Channel.objects.get_or_create(
            channel_id=self.channel_id,
            defaults={
                'name': self.channel_name,
                'last_checked': timezone.now()
            }
        )
        if created:
            avatar_file, banner_file = self.download_channel_pictures()
            channel_entry.profile_pic_path = avatar_file
            channel_entry.save()
            logger.info(f'channel created: {self.channel_name}')
        logger.debug(f'filenames dictionary: {self.filenames}')

        video_entry, created = channel_entry.video_set.get_or_create(
            video_id=self.video_id,
            defaults={
                'title': self.video_title,
                'filename': self.filenames[self.video_id],
                'description': self.video_description,
                'upload_date': datetime.strptime(self.upload_date, "%Y%m%d").date(),
                'last_checked': timezone.now()
            }
        )
        video_entry.save()
        return video_entry
