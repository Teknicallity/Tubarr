import re
import logging
from urllib.parse import urlparse, parse_qs

from videomanager.content_handlers.media_content import MediaContent
from videomanager.content_handlers.playlisthandler import PlaylistHandler
from videomanager.content_handlers.videohandler import VideoHandler

logger = logging.getLogger(__name__)


class UnknownContentTypeError(Exception):
    pass


class UnknownUrlError(Exception):
    pass


class ContentFactory:

    @classmethod
    def get_content_object(cls, url: str) -> MediaContent:
        if cls._is_valid_yt_url(url):
            try:
                content_type = cls._parse_content_type(url)
            except UnknownContentTypeError as e:
                logger.warning(f'{e}: Not a valid content type: {url}')
                raise e
            else:
                match content_type:
                    case 'channel':
                        logger.warning('Channel download not implemented')
                        raise NotImplementedError

                    case 'video':
                        return VideoHandler(url)

                    case 'playlist':
                        return PlaylistHandler(url)

        else:
            logger.warning(f'Unknown URL: {url}')
            raise UnknownUrlError

    @staticmethod
    def _parse_content_type(url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if parsed_url.path.startswith('/channel/'):
            return 'channel'
        elif parsed_url.path.startswith('/watch'):
            if playlist_id := query_params.get('list'):
                url = f'https://www.youtube.com/playlist?list={playlist_id[0]}'
                return 'playlist'
            else:
                return 'video'
        elif parsed_url.path.startswith('/playlist'):
            return 'playlist'
        else:
            raise UnknownContentTypeError

    @staticmethod
    def _is_valid_yt_url(url: str) -> bool:
        pattern = r"(https?:\/\/)?(www\.)?youtube\..+?\/"
        if re.match(pattern, url):
            return True
        else:
            return False