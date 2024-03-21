from datetime import datetime
import os.path

from videomanager.content import Content
from videomanager.models import Channel, PlaylistSource
from django.utils import timezone

from videomanager.video import Video


class Playlist(Content):
    def __init__(self, url):
        super().__init__()
        self.url = url

        self.channel_id = None
        self.channel_name = None
        self.thumbnail_url = None
        self.playlist_id = None
        self.playlist_name = None
        self.playlist_entry_count = None
        self.upload_date = None

        self.info_dict = None
        self.playlist_entries = None

    def fill_info(self):
        ydl = self._initial_ydl_opts()
        self.info_dict = ydl.extract_info(self.url, download=False)

        self.channel_id = self.info_dict['channel_id']
        self.channel_name = self.info_dict['channel']
        self.thumbnail_url = self.info_dict['thumbnails'][-1]['url']
        self.playlist_id = self.info_dict['id']
        self.playlist_name = self.info_dict['title']
        self.playlist_entry_count = self.info_dict['playlist_count']
        self.upload_date = self.info_dict['modified_date']
        self.playlist_entries = self.info_dict['entries']

    def get_info_dict(self) -> dict:
        info = {
            'type': 'playlist',
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'thumbnail_url': self.thumbnail_url,
            'playlist_id': self.playlist_id,
            'playlist_name': self.playlist_name,
            'upload_date': self.upload_date,
            'playlist_entry_count': self.playlist_entry_count,
            'playlist_entries': self.playlist_entries,
        }
        return info

    def download(self, videos_dir, config_dir):
        self.download_path = os.path.join(videos_dir, self.channel_id)

        ydl = self._get_download_opts(config_dir)
        ydl.download(self.url)

        # return self.download_path, self.filename

    def insert_into_db(self):
        playlist_source = PlaylistSource.objects.get_or_create(name='temporary')
        channel_entry = Channel.objects.get(channel_id=self.channel_id)
        new_playlist = channel_entry.playlist_set.create(
            playlist_id=self.playlist_id,
            name=self.playlist_name,
            last_checked=timezone.now(),
            source=playlist_source
        )

        for entry in self.playlist_entries:
            video = Video(ytdlp_info=entry)
            video.fill_info()
            video.filenames = self.filenames
            video_db_entry = video.insert_into_db()

            new_playlist.videos.add(video_db_entry)
