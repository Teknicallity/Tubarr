from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.test import TestCase

from videomanager.models import Video, Channel


class VideoTestCase(TestCase):
    fixtures = ['test_content']

    def test_delete_video(self):
        video = Video.objects.get(pk=1)
        video.delete()
        with self.assertRaises(Video.DoesNotExist):
            Video.objects.get(pk=video.id)

    def test_save_video(self):
        channel = Channel.objects.get(pk=1)
        video_id = 'Testvideosaving'
        filename = '[Testvideosaving]-Test_Video_Saving.txt'
        video = Video.objects.create(
            video_id=video_id,
            channel=channel,
            title='Test Video Saving',
            filename=filename,
            upload_date=datetime.now(tz=get_current_timezone()),
            last_checked=datetime.now(tz=get_current_timezone()),
            status=Video.STATUS.DOWNLOADED,
        )
        video.save()
        local_file_path = f'{video.channel.channel_id}/{video.filename}'
        self.assertEqual(video.file.name, local_file_path)
