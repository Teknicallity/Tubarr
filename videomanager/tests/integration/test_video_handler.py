import os

from django.conf import settings
from django.test import TestCase

from videomanager.content_handlers.content_handler import ContentHandler


class TestVideoHandler(TestCase):
    def setUp(self):
        pass

    def test_unknown_content_type(self):
        pass

    def test_unknown_url(self):
        pass

    def test_fill_info_video(self):
        url = 'https://www.youtube.com/watch?v=tSVNrZlWzIg'
        handler = ContentHandler(url)
        handler.fill_info()
        self.assertEqual(handler.content_object.video_id, 'tSVNrZlWzIg')
        self.assertEqual(handler.content_object.channel_id, 'UCYzzcdVEQd37sh_FNDH3ByA')
        self.assertEqual(handler.content_object.video_title, 'Asus Zenpad 8.0 Video Test')
        self.assertEqual(handler.content_object.upload_date, '20151214')
        self.assertEqual(handler.content_object.video_description,
                         'Purely for illustration purposes on a review.')

    def test_download_video(self):
        url = 'https://www.youtube.com/watch?v=tSVNrZlWzIg'
        info_dict = {'type': 'video', 'url': 'https://www.youtube.com/watch?v=tSVNrZlWzIg',
                     'video_title': 'Asus Zenpad 8.0 Video Test', 'video_id': 'tSVNrZlWzIg',
                     'video_description': 'Purely for illustration purposes on a review.',
                     'video_categories': ['Science & Technology'],
                     'video_tags': ['ASUS (Computer Manufacturer/Brand)', 'Tablet Computer (Video Game Platform)',
                                    'zenpad', '8.0', 'video', 'sample'], 'channel_id': 'UCYzzcdVEQd37sh_FNDH3ByA',
                     'channel_name': 'Gareth Myles',
                     'thumbnail_url': 'https://i.ytimg.com/vi_webp/tSVNrZlWzIg/maxresdefault.webp',
                     'upload_date': '20151214', 'filenames': {'t': 'emp'}, 'downloaded': False}

        handler = ContentHandler(url)
        handler.apply_json(info_dict)
        handler.download(insert_to_db=False, no_ytdlp_archive=True)

        filename = '[tSVNrZlWzIg]-Asus_Zenpad_8.0_Video_Test.mp4'
        full_path = os.path.join(settings.MEDIA_ROOT, handler.content_object.channel_id, filename)
        channel_path = os.path.join(settings.MEDIA_ROOT, handler.content_object.channel_id)

        self.assertTrue(os.path.exists(channel_path))
        self.assertTrue(os.path.isfile(full_path))

        os.remove(full_path)
        os.rmdir(channel_path)

        self.assertFalse(os.path.exists(channel_path))
