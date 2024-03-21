import yt_dlp
import os.path


class Content:
    # url = None
    #
    # video_title = None
    # video_id = None
    # video_description = None
    # video_categories = None
    # video_tags = None
    # channel_id = None
    # channel_name = None
    # channel_pic = None
    # thumbnail_url = None
    # playlist_id = None
    # playlist_name = None
    # playlist_entry_count = None
    # upload_date = None
    #
    # playlist_entries = None
    # content_type = None
    # filename = None
    # download_path = None
    # downloaded = False

    def __init__(self):
        self.download_path = None
        self.filenames: dict = {}
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

    def _ytdl_hook(self, d):
        if d['status'] == 'finished':
            if d['info_dict']:
                filename = os.path.basename(d.get('info_dict').get('_filename'))

                video_id = d.get('info_dict').get('_filename')
                self.filenames[video_id] = filename
                self.downloaded = True

    def download(self, videos_dir, config_dir):
        pass

    def fill_info(self):
        pass

    def get_info_dict(self) -> dict:
        pass
