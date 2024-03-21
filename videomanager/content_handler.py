import os.path
import re
from urllib.parse import urlparse, parse_qs
from enum import Enum
import yt_dlp
import json

from videomanager.content import Content
from videomanager.playlist import Playlist
from videomanager.video import Video


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


class ContentHandler:
    def __init__(self, url: str):
        self.url = url
        self.content_object: Content = Content()
        self.content_type = None

    def fill_info(self):
        """Parses the url"""
        if _is_valid_url(self.url):
            try:
                self.content_type = _parse_content_type(self.url)
            except UnknownContentTypeError as e:
                raise e

            match self.content_type:
                case 'channel':
                    print("channel")

                case 'video':
                    print("Video")
                    self.content_object = Video(self.url)
                    self.content_object.fill_info()

                case 'playlist':
                    print("playlist")
                    self.content_object = Playlist(self.url)
                    self.content_object.fill_info()

                case _:
                    print("error")
        else:
            raise UnknownUrlError

    def get_info_dict(self) -> dict:
        return self.content_object.get_info_dict()

    def download(self, videos_dir, config_dir):
        self.content_object.download(videos_dir, config_dir)



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
