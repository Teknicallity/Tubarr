from functools import lru_cache

import logging
import requests
import os
import shutil
import yt_dlp
from django.conf import settings

from videomanager.content_handlers.ytdlp_logger import YtDlpLogger
from videomanager.content_handlers.ytdlp_options import YdlDownloadOptions

logger = logging.getLogger(__name__)


class Ydl:

    def __init__(self):
        pass

    @staticmethod
    @lru_cache(maxsize=10)
    def get_yt_info(url: str) -> dict:
        options = {
            'restrictfilenames': True,
            'forceprint': True,
            'format': 'best',
            'quiet': True,
        }
        return yt_dlp.YoutubeDL(options).extract_info(url, download=False)

    @staticmethod
    def download_channel_picture(channel_id: str) -> (str, str):
        download_path = os.path.join(settings.MEDIA_ROOT, channel_id)
        avatar_url, banner_url = _get_channel_pictures_url(channel_id)
        avatar_name = ''
        banner_name = ''

        if avatar_url != '':
            avatar_name = 'avatar.jpg'
            avatar_path = os.path.join(download_path, avatar_name)
            _download_picture(avatar_url, avatar_path)
        else:
            logger.warning(f"could not get avatar url for {channel_id}")

        if banner_url != '':
            banner_name = 'banner.jpg'
            banner_path = os.path.join(download_path, banner_name)
            _download_picture(banner_url, banner_path)
        else:
            logger.warning(f"could not get banner url for {channel_id}")

        return avatar_name, banner_name

    @staticmethod
    def download(url: str, ydl_opts: YdlDownloadOptions):
        os.makedirs(os.path.join(settings.CONFIG_DIR, 'ytdlp'), exist_ok=True)
        options = {
            'restrictfilenames': True,
            'format': 'best',
            'quiet': True,
            'logger': YtDlpLogger(ydl_opts.trigger_string, ydl_opts.trigger_callback),
            'progress_hooks': [ydl_opts.ytdlp_hook],
            'paths': {'home': ydl_opts.download_path},
            'outtmpl': {'default': '[%(id)s]-%(title)s.%(ext)s'},
            'download_archive': os.path.join(settings.CONFIG_DIR, 'ytdlp', 'downloaded.txt'),
        }
        if not ydl_opts.ydl_download_tracker:
            del options['download_archive']

        yt_dlp.YoutubeDL(options).download(url)


def _get_channel_pictures_url(channel_id: str) -> (str, str):
    ydl = yt_dlp.YoutubeDL({'playlist_items': '0'})
    info = ydl.extract_info('www.youtube.com/channel/' + channel_id)
    avatar = ''
    banner = ''

    for image_dict in info['thumbnails']:
        image_dict: dict
        if image_dict.get('id') == 'avatar_uncropped':
            avatar = image_dict.get('url')
        elif image_dict.get('id') == 'banner_uncropped':
            banner = image_dict.get('url')

    return avatar, banner


def _download_picture(url: str, path: str):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    else:
        logger.warning(f"Could not download picture")
