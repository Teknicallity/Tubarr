import shutil

import requests
import yt_dlp
import os.path


class Content:

    def __init__(self):
        self.download_path = None
        self.downloaded = False
        self.channel_id = None
        self.channel_name = None
        self.filenames = {'t': 'emp'}

    @staticmethod
    def _initial_ydl_opts() -> yt_dlp.YoutubeDL:  # add error hook?
        ydl_opts = {
            'restrictfilenames': True,
            'forceprint': True,
            'format': 'best',
            'quiet': True,
        }
        return yt_dlp.YoutubeDL(ydl_opts)

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

    def download_channel_pictures(self) -> (str, str):
        avatar_url, banner_url = self._get_channel_pictures_url(self.channel_id)
        avatar_name = ''
        banner_name = ''

        if avatar_url != '':
            avatar_name = 'avatar.jpg'
            avatar_path = os.path.join(self.download_path, avatar_name)
            self._download_picture(avatar_url, avatar_path)
        else:
            print(f"could not get avatar url for {self.channel_name}\n")

        if banner_url != '':
            banner_name = 'banner.jpg'
            banner_path = os.path.join(self.download_path, banner_name)
            self._download_picture(banner_url, banner_path)
        else:
            print(f"could not get banner url for {self.channel_name}\n")

        return avatar_name, banner_name

    @staticmethod
    def _download_picture(url: str, path: str):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        else:
            print('Could not download picture')

    @staticmethod
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

    def _ytdl_hook(self, d):
        if d['status'] == 'finished':
            if d['info_dict']:
                filename = os.path.basename(d.get('info_dict').get('filename'))

                video_id = d.get('info_dict').get('id')
                self.downloaded = True
                print('\nVIDEOID AT HOOK:', video_id)
                print('\nVIDEONAME AT HOOK:', filename)
                self.filenames[video_id] = filename

    def download(self, videos_dir, config_dir):
        pass

    def fill_info(self):
        pass

    def get_info_dict(self) -> dict:
        pass

    def insert_into_db(self):
        pass

