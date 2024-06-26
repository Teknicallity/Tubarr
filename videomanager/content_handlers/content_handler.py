import re
import logging
from urllib.parse import urlparse, parse_qs

from videomanager.content_handlers.content import Content
from videomanager.content_handlers.playlist import Playlist
from videomanager.content_handlers.video import Video

from django_huey import task

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

logger = logging.getLogger(__name__)


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
                self.content_type = self._parse_content_type()
            except UnknownContentTypeError as e:
                logger.warning(f'{e}: Not a valid content type: {self.url}')
                raise e

            match self.content_type:
                case 'channel':
                    logger.warning('Channel download not implemented')

                case 'video':
                    self.content_object = Video(self.url)
                    self.content_object.fill_info()

                case 'playlist':
                    self.content_object = Playlist(self.url)
                    self.content_object.fill_info()

        else:
            logger.warning(f'Unknown URL: {self.url}')
            raise UnknownUrlError

    def get_attribute_dict(self) -> dict:
        return self.content_object.get_attribute_dict()

    def download(self, insert_to_db: bool = True, no_ytdlp_archive: bool = False, download_path: str = None):
        self.content_object.download(no_ytdlp_archive, download_path)

        if insert_to_db and self.content_object.downloaded:
            self.content_object.insert_into_db()

    def apply_json(self, info: dict):
        match info['type']:
            case 'channel':
                logger.warning('Channel attributes not implemented')

            case 'video':
                self.content_object = Video()
                self.content_object.__dict__ = info

            case 'playlist':
                self.content_object = Playlist()
                self.content_object.__dict__ = info

    def _parse_content_type(self) -> str:
        parsed_url = urlparse(self.url)
        query_params = parse_qs(parsed_url.query)
        if parsed_url.path.startswith('/channel/'):
            return 'channel'
        elif parsed_url.path.startswith('/watch'):
            if playlist_id := query_params.get('list'):
                self.url = f'https://www.youtube.com/playlist?list={playlist_id[0]}'
                return 'playlist'
            else:
                return 'video'
        elif parsed_url.path.startswith('/playlist'):
            return 'playlist'
        else:
            raise UnknownContentTypeError


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
