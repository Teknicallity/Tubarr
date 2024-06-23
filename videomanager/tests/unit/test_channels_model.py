from django.test import TestCase

from videomanager.models import Channel


class ChannelTestCase(TestCase):
    fixtures = ['test_content']

    def test_channel_is_empty(self):
        channel = Channel.objects.get(pk=1)
        self.assertEqual(channel.is_empty(), False)
        channel.video_set.all().delete()
        self.assertEqual(channel.is_empty(), True)

        channel = Channel.objects.get(pk=2)
        channel.video_set.all().delete()
        self.assertEqual(channel.is_empty(), False)
        channel.playlist_set.all().delete()
        self.assertEqual(channel.is_empty(), True)

    def test_channel_delete(self):
        channel = Channel.objects.get(pk=1)
        channel.delete()
        with self.assertRaises(Channel.DoesNotExist):
            Channel.objects.get(pk=channel.pk)
