import os.path
import re
from urllib.parse import urlparse, parse_qs
from enum import Enum
import yt_dlp
import json


# yt-dlp --flat-playlist --print-to-file webpage_url "TEXT_FILE.txt" "CHANNEL_URL"

# yt-dlp --flat-playlist --print "pre_process:Playlist - %(title)s - %(id)s" --exec "pre_process:yt-dlp %(url)q
#   --flat-playlist --print \"Video - %%(title)s - %%(id)s\""
#   "https://www.youtube.com/@3blue1brown/playlists?view=1&sort=dd&shelf_id=0"

# download_archive: file
# --download-archive FILE Download only media not listed in the archive file.
# Record the IDs of all downloaded media in it

# -P FILEPATH

# forceprint:
# ffmpeg_location:

# grab all media in a playlist, make each a video object with an optional attribute playlist id
# for each video , download. put them in a queue, then for each with x media at a time


# cannot use with json serializing
# class _URLType(Enum):
#     CHANNEL = 1
#     VIDEO = 2
#     PLAYLIST = 3
#     UNKNOWN = 4

class UnknownContentTypeError(Exception):
    pass


class UnknownUrlError(Exception):
    pass


def initial_ydl_opts() -> yt_dlp.YoutubeDL:  # add error hook?
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
        self.playlist_entry_count = None
        self.upload_date = None

        self.playlist_entries = None
        self.content_type = None
        self.filename = None
        self.download_path = None
        self.downloaded = False

    def fill_info(self):
        """Parses the url"""
        if _is_valid_url(self.url):
            ydl = initial_ydl_opts()
            try:
                self.content_type = _parse_content_type(self.url)
            except UnknownContentTypeError as e:
                raise e

            match self.content_type:
                case 'channel':
                    print("channel")

                case 'video':
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

                case 'playlist':
                    print("playlist")
                    info_dict = ydl.extract_info(self.url, download=False)
                    self.video_title = None
                    self.video_id = None
                    self.video_description = None
                    self.video_categories = None
                    self.video_tags = None
                    self.channel_id = info_dict['channel_id']
                    self.channel_name = info_dict['channel']
                    self.channel_pic = None
                    self.thumbnail_url = info_dict['thumbnails'][-1]['url']
                    self.playlist_id = info_dict['id']
                    self.playlist_name = info_dict['title']
                    self.playlist_entry_count = info_dict['playlist_count']
                    self.upload_date = info_dict['modified_date']
                    self.playlist_entries = info_dict['entries']

                case _:
                    print("error")
        else:
            raise UnknownUrlError

    def get_info_dict(self) -> dict:
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
            'playlist_entry_count': self.playlist_entry_count,
        }
        return info

    def download(self, videos_dir, config_dir) -> (str, str):
        self.download_path = os.path.join(videos_dir, self.channel_id)

        ydl = self._get_download_opts(config_dir)
        ydl.download(self.url)

        return self.download_path, self.filename

    def _get_download_opts(self, config_dir) -> yt_dlp.YoutubeDL:
        ydl_opts = {
            'restrictfilenames': True,
            'format': 'best',
            'quiet': True,
            'progress_hooks': [self._ytdl_hook],
            'paths': {'home': self.download_path},
            'outtmpl': {'default': '[%(id)s]-%(title)s.%(ext)s'},
            # 'download_archive': os.path.join(config_dir, 'ytdlp', 'downloaded.txt'),
        }
        return yt_dlp.YoutubeDL(ydl_opts)

    def _ytdl_hook(self, d):
        if d['status'] == 'finished':
            if d['info_dict']:
                self.filename = os.path.basename(d.get('info_dict').get('_filename'))
                self.downloaded = True
            # VIDEO SAVE


def _is_valid_url(url: str) -> bool:
    """
    Validates given url is a Youtube URL
    @param url: URL to validate
    @return:
    """
    pattern = r"(https?:\/\/)?(www\.)?youtube\..+?\/"
    if re.match(pattern, url):
        return True
    else:
        return False
    # return True if re.search(pattern, url) else False


def _parse_content_type(url: str) -> str:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if parsed_url.path.startswith('/channel/'):
        return 'channel'
    elif parsed_url.path.startswith('/watch'):
        if 'list' in query_params:
            return 'playlist'
        else:
            return 'video'
    elif parsed_url.path.startswith('/playlist'):
        return 'playlist'
    else:
        raise UnknownContentTypeError
