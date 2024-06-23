from django.test import TestCase

from videomanager.models import Playlist, Video


class PlaylistTestCase(TestCase):
    fixtures = ['test_content']

    def test_playlist_delete(self):
        playlist = Playlist.objects.get(pk=1)
        videos = playlist.videos.all()
        playlist.delete()
        with self.assertRaises(Playlist.DoesNotExist):
            Playlist.objects.get(pk=playlist.id)
        for video in videos:
            with self.assertRaises(Video.DoesNotExist):
                Video.objects.get(pk=video.id)
