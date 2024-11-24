import time
from functools import lru_cache

import logging
import requests
import os
import shutil
import yt_dlp
from django.conf import settings
import django_huey
from huey import signals

from videomanager.content_handlers.ytdlp_logger import YtDlpLogger
from videomanager.content_handlers.ytdlp_options import YdlDownloadOptions
from videomanager.models import Video

logger = logging.getLogger(__name__)


class Ydl:

    def __init__(self):
        pass

    @staticmethod
    @lru_cache(maxsize=10)
    def get_yt_info(url: str) -> dict:
        os.makedirs(os.path.join(settings.CONFIG_DIR, 'ytdlp'), exist_ok=True)
        options = {
            'restrictfilenames': True,
            'forceprint': True,
            'format': 'best',
            'quiet': True,
            'cachedir': os.path.join(settings.CONFIG_DIR, 'ytdlp', 'cache'),
        }
        cookie_filepath = os.path.join(settings.CONFIG_DIR, 'ytdlp', 'cookies.txt')
        if os.path.isfile(cookie_filepath):
            options['cookiefile'] = cookie_filepath
        return yt_dlp.YoutubeDL(options).extract_info(url, download=False)

    @staticmethod
    def download_channel_picture(channel_id: str) -> (str, str):
        download_path = os.path.join(settings.MEDIA_ROOT, channel_id)
        os.makedirs(download_path, exist_ok=True)

        if settings.DEMO_MODE:
            _copy_demo_resources(download_path)
            return 'avatar.jpg', 'banner.jpg'

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
    def download_thumbnail(thumbnail_url: str, channel_id: str, output_basename: str) -> str:
        # https://stackoverflow.com/questions/49825421/download-file-using-python-without-knowing-its-extension-content-type-strea
        absolute_thumbnails_dir = os.path.join(settings.MEDIA_ROOT, channel_id, "thumbnails")
        os.makedirs(absolute_thumbnails_dir, exist_ok=True)

        if settings.DEMO_MODE:
            thumbnail_filepath = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
            if not os.path.isfile(thumbnail_filepath):
                shutil.copyfile(
                    os.path.join(settings.DEMO_DIR, 'thumbnail.jpg'),
                    thumbnail_filepath
                )

            return thumbnail_filepath

        r = requests.get(thumbnail_url)
        extension = r.headers['content-type'].split('/')[-1]
        absolute_thumbnail_filepath = os.path.join(absolute_thumbnails_dir, f"{output_basename}.{extension}")

        with open(absolute_thumbnail_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

        return os.path.join(channel_id, "thumbnails", f"{output_basename}.{extension}")

    @staticmethod
    @django_huey.task()
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
            'cachedir': os.path.join(settings.CONFIG_DIR, 'ytdlp', 'cache'),
            # 'writethumbnail': True,  # writes to the given paths home directory, not thumbnails directory
        }
        cookie_filepath = os.path.join(settings.CONFIG_DIR, 'ytdlp', 'cookies.txt')
        if os.path.isfile(cookie_filepath):
            options['cookiefile'] = cookie_filepath
        if not ydl_opts.track_with_ytdlp_archive:
            del options['download_archive']

        if settings.DEMO_MODE:
            options['skip_download'] = True

        yt_dlp.YoutubeDL(options).download(url)

    @staticmethod
    @django_huey.signal(signals.SIGNAL_EXECUTING)
    def print_executing(signal, task):
        logger.info('SCHEDULED: %s - %s' % (signal, task.id))  # SCHEDULED: executing - fdc8829d-d52f-4cb1-8307-af2f1666e0dc

    @staticmethod
    @django_huey.signal(signals.SIGNAL_ERROR, signals.SIGNAL_CANCELED)
    def print_executing(signal, task, exc=None):
        logger.warning('ERROR: %s - %s' % (signal, task.id))
        if exc:
            logger.warning(exc)

    @staticmethod
    @django_huey.task()
    def demo_download(video_id: str, channel_id: str):
        time.sleep(5)
        shutil.copyfile(
            os.path.join(settings.DEMO_DIR, '[Wtwyosdkx44] Doot Doot Mr Skeltal Original.mp4'),
            os.path.join(settings.MEDIA_ROOT, channel_id, '[Wtwyosdkx44] Doot Doot Mr Skeltal Original.mp4')
        )
        v = Video.objects.get(video_id=video_id)
        v.filename = '[Wtwyosdkx44] Doot Doot Mr Skeltal Original.mp4'
        v.status = v.STATUS.DOWNLOADED
        v.save()


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


def _download_picture(url: str, filepath: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        logger.info(f"Downloaded picture from {url} to {filepath}")

    except requests.RequestException as e:
        logger.warning(f"Could not download picture from {url}: {e}")
    except FileNotFoundError as e:
        logger.error(f"File not found error when saving picture to {filepath}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def _copy_demo_resources(download_path):
    thumbnail_filepath = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
    if not os.path.isfile(thumbnail_filepath):
        shutil.copyfile(
            os.path.join(settings.DEMO_DIR, 'thumbnail.jpg'),
            thumbnail_filepath
        )
    shutil.copyfile(
        os.path.join(settings.DEMO_DIR, 'avatar.jpg'),
        os.path.join(download_path, 'avatar.jpg')
    )
    shutil.copyfile(
        os.path.join(settings.DEMO_DIR, 'banner.jpg'),
        os.path.join(download_path, 'banner.jpg')
    )