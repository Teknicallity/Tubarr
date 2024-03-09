import os.path
import re
from urllib.parse import urlparse, parse_qs
from enum import Enum
import yt_dlp
import json


# download_archive: file
# --download-archive FILE Download only videos not listed in the archive file.
# Record the IDs of all downloaded videos in it

# -P FILEPATH

# forceprint:
# ffmpeg_location:


class _URLType(Enum):
    CHANNEL = 1
    VIDEO = 2
    PLAYLIST = 3
    UNKNOWN = 4


def initial_ydl_opts() -> yt_dlp.YoutubeDL:
    ydl_opts = {
        'restrictfilenames': True,
        'forceprint': True,
        'format': 'best',
        'quiet': True,
    }
    return yt_dlp.YoutubeDL(ydl_opts)


class Content:
    def __init__(self, url: str):
        self.url = url

        self.video_title = None
        self.video_id = None
        self.video_description = None
        self.video_categories = None
        self.video_tags = None
        self.channel_id = None
        self.channel_name = None
        self.channel_pic = None
        self.thumbnail_url = None
        self.playlist_id = None
        self.playlist_name = None
        self.upload_date = None

        self.content_type = None
        self.filename = None
        self.download_path = None
        self.info: dict = {}

    def fill_info(self):
        """Parses the url"""
        if _is_valid_url(self.url):
            ydl = initial_ydl_opts()
            self.content_type = _parse_content_type(self.url)

            match self.content_type:
                case _URLType.CHANNEL:
                    print("channel")

                case _URLType.VIDEO:
                    print("Video")
                    info_dict = ydl.extract_info(self.url, download=False)
                    self.video_title = info_dict['title']
                    self.video_id = info_dict['id']
                    self.video_description = info_dict['description']
                    self.video_categories = info_dict['categories']
                    self.video_tags = info_dict['tags']
                    self.channel_id = info_dict['channel_id']
                    self.channel_name = info_dict['channel']
                    self.thumbnail_url = info_dict['thumbnail']
                    self.upload_date = info_dict['upload_date']

                case _URLType.PLAYLIST:
                    print("playlist")

                case _:
                    print("error")

    def _get_json_info(self) -> str:
        info = {
            'type': self.content_type,
            'video_title': self.video_title,
            'video_id': self.video_id,
            'video_description': self.video_description,
            'video_categories': self.video_categories,
            'video_tags': self.video_tags,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'thumbnail_url': self.thumbnail_url,
            'playlist_id': self.playlist_id,
            'playlist_name': self.playlist_name,
            'channel_pic': self.channel_pic,
            'upload_date': self.upload_date,
        }
        return json.dumps(info)

    def download(self, videos_dir, config_dir) -> (str, str):
        self.download_path = os.path.join(videos_dir, self.channel_id)

        ydl = self._get_download_opts(config_dir)
        ydl.download(self.url)

        return self.download_path, self.filename

    def _get_download_opts(self, config_dir) -> yt_dlp.YoutubeDL:
        ydl_opts = {
            'restrictfilenames': True,
            'forceprint': True,
            'format': 'best',
            # 'quiet': True,
            'progress_hooks': [self._ytdl_hook],
            'outtmpl': os.path.join(self.download_path, '%(title)s-[%(id)s].%(ext)s'),
            'download_archive': os.path.join(config_dir, 'ytdlp', 'downloaded.txt'),
        }
        return yt_dlp.YoutubeDL(ydl_opts)

    def _ytdl_hook(self, d):
        if d['status'] == 'finished':
            if d['info_dict']:
                self.filename = d['info_dict']['_filename']


def _is_valid_url(url: str) -> bool:
    """
    Validates given url is a Youtube URL
    @param url: URL to validate
    @return:
    """
    pattern = r"(https?:\/\/)?(www\.)?youtube\..+?\/"
    if re.search(pattern, url):
        return True
    else:
        return False
    # return True if re.search(pattern, url) else False


def _parse_content_type(url: str) -> _URLType:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if parsed_url.path.startswith('/channel/'):
        return _URLType.CHANNEL
    elif parsed_url.path.startswith('/watch'):
        if 'list' in query_params:
            return _URLType.PLAYLIST
        else:
            return _URLType.VIDEO
    else:
        return _URLType.UNKNOWN
