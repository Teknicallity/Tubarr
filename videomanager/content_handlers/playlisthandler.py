import os.path
import logging

from videomanager.content_handlers.media_content import MediaContent
from videomanager.content_handlers.ytdlp import Ydl
from videomanager.content_handlers.ytdlp_options import YdlDownloadOptions
from videomanager.models import Channel, PlaylistSource
from django.utils import timezone
from django.conf import settings

from videomanager.content_handlers.videohandler import VideoHandler

logger = logging.getLogger(__name__)


class PlaylistHandler(MediaContent):
    def __init__(self, url: str = None):
        super().__init__()
        self.url = url

    def fill_info(self):
        self.info_dict = Ydl.get_yt_info(self.url)

        self.channel_id = self.info_dict['channel_id']
        self.channel_name = self.info_dict['channel']
        self.thumbnail_url = self.info_dict['thumbnails'][-1]['url']
        self.playlist_id = self.info_dict['id']
        self.playlist_name = self.info_dict['title']
        self.playlist_entry_count = self.info_dict['playlist_count']
        self.upload_date = self.info_dict['modified_date']
        self.playlist_entries = self.info_dict['entries']

    def get_attribute_dict(self) -> dict:
        info = {
            'type': 'playlist',
            'url': self.url,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'thumbnail_url': self.thumbnail_url,
            'playlist_id': self.playlist_id,
            'playlist_name': self.playlist_name,
            'upload_date': self.upload_date,
            'playlist_entry_count': self.playlist_entry_count,
            'playlist_entries': self.playlist_entries,
            'filenames': self.filenames,
            'downloaded': self.downloaded,
        }
        return info

    def download(self, track_with_ytdlp_archive: bool = True):
        self.insert_info_into_db()

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
        playlist_source, created = PlaylistSource.objects.get_or_create(name='youtube')
        channel_entry = super().insert_info_into_db()

        new_playlist = channel_entry.playlist_set.create(
            playlist_id=self.playlist_id,
            name=self.playlist_name,
            last_checked=timezone.now(),
            source=playlist_source
        )

        for entry in self.playlist_entries:
            video = VideoHandler(ytdlp_info=entry)
            video.fill_info()
            video_db_entry = video.insert_info_into_db()

            new_playlist.videos.add(video_db_entry)
