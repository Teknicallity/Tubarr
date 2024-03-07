import re
from urllib.parse import urlparse, parse_qs
from enum import Enum
import yt_dlp


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


def temp_grab_json() -> yt_dlp.YoutubeDL:
    ydl_opts = {
        'restrictfilenames': True,
        'forceprint': True,
        'format': 'best',
        'quiet': True,
    }
    return yt_dlp.YoutubeDL(ydl_opts)


class Content:
    def __init__(self, url: str):
        # self.video_title = None
        # self.video_id = None
        # self.video_description = None
        # self.video_categories = None
        # self.video_tags = None
        # self.channel_id = None
        # self.channel_name = None
        # self.thumbnail_url = None
        # self.playlist_id = None
        # self.playlist_name = None
        # self.channel_pic = None
        # self.upload_date = None
        self.info: dict = {}

        """Parses the url"""
        if _is_valid_url(url):
            ydl = temp_grab_json()
            tag = _parse_url(url)
            match tag:
                case _URLType.CHANNEL:
                    print("channel")
                case _URLType.VIDEO:
                    print("Video")
                    """
                    Grab:
                    id
                    title
                    thumbnail
                    description
                    channel_id
                    categories
                    tags
                    upload_date
                    original_url
                    """
                    info_dict = ydl.extract_info(url, download=False)
                    self.info = {
                        'type': 'video',
                        'video_id': info_dict['id'],
                        'video_title': info_dict['title'],
                        'thumbnail_url': info_dict['thumbnail'],
                        'video_description': info_dict['description'],
                        'channel_id': info_dict['channel_id'],
                        'video_categories': info_dict['categories'],
                        'video_tags': info_dict['tags'],
                        'channel_name': info_dict['channel'],
                        'upload_date': info_dict['upload_date']
                    }
                case _URLType.PLAYLIST:
                    print("playlist")
                case _:
                    print("error")


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


def _parse_url(url: str) -> _URLType:
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
