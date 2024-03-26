import yt_dlp
import os.path


class Content:

    def __init__(self):
        self.download_path = None
        self.downloaded = False

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

    def _ytdl_hook(self, d):  # try making this function in each object
        pass

    def download(self, videos_dir, config_dir):
        pass

    def fill_info(self):
        pass

    def get_info_dict(self) -> dict:
        pass
