import logging
import os

logger = logging.getLogger(__name__)


class MediaContent:

    def __init__(self):
        self.download_path = None
        self.downloaded = False
        self.channel_id = None
        self.channel_name = None
        self.type = None
        self.filenames = {'t': 'emp'}

        self.video_title = None
        self.video_id = None
        self.video_description = None
        self.video_categories = None
        self.video_tags = None
        self.thumbnail_url = None
        self.upload_date = None

        self.playlist_id = None
        self.playlist_name = None
        self.playlist_entry_count = None

        self.info_dict = None
        self.playlist_entries = None

    def _get_existing_video_log_identifier(self):
        if self.type and self.type == 'video':
            return ": has already been recorded in the archive"
        else:
            return None

    def _set_already_downloaded(self, found_message):
        # self.downloaded = True
        # found from ytdlp archive file
        #   "[download] lvaWJs9KZTI: has already been recorded in the archive"
        # found video file existing. not in archive.
        #   [download] C:\Users\Josh\Documents\Web_Dev\Tubarr\media\UC4w1YQAJMWOz4qtxinq55LQ\[lvaWJs9KZTI]-New_Intel_Motherboards_A770_AI_Demos_Arc_GPUs_and_MORE_-_Intel_@_ASRock_s_Computex_2024_Booth.mp4 has already been downloaded
        # video exists, but downloading playist
        exists_in_archive = ': has already been recorded in the archive'
        exists_on_disk = ' has already been downloaded'
        if exists_in_archive in found_message:
            # check if on disk
            pass
        elif exists_on_disk in found_message:
            pass
        return print(f'FOUND ALREADY DOWNLAODED: {found_message}')

    def _ytdl_hook(self, d):
        if d['status'] == 'finished':
            if d['info_dict']:
                filename = os.path.basename(d.get('info_dict').get('filename'))

                video_id = d.get('info_dict').get('id')
                self.downloaded = True
                logger.debug(f'Video Id At Ytdl Hook: {video_id}')
                logger.debug(f'Video Name At Ytdl Hook: {filename}')
                self.filenames[video_id] = filename

    def download(self, ydl_download_tracker: bool = True):
        raise NotImplementedError

    def fill_info(self):
        raise NotImplementedError

    def get_attribute_dict(self) -> dict:
        raise NotImplementedError

    def insert_into_db(self):
        raise NotImplementedError
