import os
import shutil

from django.conf import settings
from django.test import TestCase

from videomanager.content_handlers.content_factory import ContentFactory


class TestVideoHandler(TestCase):
    def setUp(self):
        pass

    def test_unknown_content_type(self):
        pass

    def test_unknown_url(self):
        pass

    def test_fill_info_video(self):
        url = 'https://www.youtube.com/watch?v=tSVNrZlWzIg'
        content = ContentFactory.get_content_object(url)
        content.fill_info()
        self.assertEqual(type(content).__name__, 'VideoHandler')
        self.assertEqual(content.video_id, 'tSVNrZlWzIg')
        self.assertEqual(content.channel_id, 'UCYzzcdVEQd37sh_FNDH3ByA')
        self.assertEqual(content.video_title, 'Asus Zenpad 8.0 Video Test')
        self.assertEqual(content.upload_date, '20151214')
        self.assertEqual(content.video_description,
                         'Purely for illustration purposes on a review.')

    def test_download_video(self):
        url = 'https://www.youtube.com/watch?v=tSVNrZlWzIg'

        content = ContentFactory.get_content_object(url)
        content.fill_info()
        content.download(track_with_ytdlp_archive=False)

        filename = '[tSVNrZlWzIg]-Asus_Zenpad_8.0_Video_Test.mp4'
        full_path = os.path.join(settings.MEDIA_ROOT, content.channel_id, filename)
        channel_path = os.path.join(settings.MEDIA_ROOT, content.channel_id)

        self.assertTrue(os.path.exists(channel_path))
        self.assertTrue(os.path.isfile(full_path))
        shutil.rmtree(channel_path)

        self.assertFalse(os.path.exists(channel_path))
