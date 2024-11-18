from datetime import datetime
import os.path
import logging

from videomanager.content_handlers.media_content import MediaContent
from videomanager.content_handlers.ytdlp import Ydl
from videomanager.content_handlers.ytdlp_options import YdlDownloadOptions
from videomanager.models import Channel, Video
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


class VideoHandler(MediaContent):
    def __init__(self, url: str = None, ytdlp_info=None):
        super().__init__()
        self.url = url

        self.info_dict = ytdlp_info

    def fill_info(self):
        if self.info_dict is None:
            self.info_dict = Ydl.get_yt_info(self.url)

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

    def download(self, track_with_ytdlp_archive: bool = True):
        self.insert_info_into_db()

        if settings.DEMO_MODE:
            Ydl.demo_download(self.video_id, self.channel_id)
            return

        self.download_path = os.path.join(settings.MEDIA_ROOT, self.channel_id)
        options = YdlDownloadOptions(
            trigger_string=[': has already been recorded in the archive'],
            trigger_callback=self._set_already_downloaded,
            ytdlp_hook=self._ytdl_hook,
            download_path=f'{self.download_path}',
            track_with_ytdlp_archive=track_with_ytdlp_archive
        )
        Ydl.download(self.url, options)

        # return self.download_path, self.filename

    def insert_info_into_db(self):
        channel_entry = super().insert_info_into_db()
        logger.debug(f'filenames dictionary: {self.filenames}')

        video_entry, created = channel_entry.video_set.get_or_create(
            video_id=self.video_id,
            defaults={
                'title': self.video_title,
                'description': self.video_description,
                'upload_date': datetime.strptime(self.upload_date, "%Y%m%d").date(),
                'last_checked': timezone.now(),
                'status': Video.STATUS.QUEUED,
            }
        )
        video_entry.save()
        return video_entry
