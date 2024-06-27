from django.test import TestCase

from videomanager.content_handlers.content_factory import ContentFactory


class TestPlaylistHandler(TestCase):

    def test_fill_info_playlist(self):
        url = 'https://www.youtube.com/playlist?list=PL10NWKboioZT3cOSnRtX0oEghpj_4wKAv'
        content = ContentFactory.get_content_object(url)
        content.fill_info()
        self.assertEqual(type(content).__name__, 'Playlist')
        self.assertEqual(content.playlist_id, 'PL10NWKboioZT3cOSnRtX0oEghpj_4wKAv')
        self.assertEqual(content.channel_id, 'UC4w1YQAJMWOz4qtxinq55LQ')
        self.assertEqual(content.playlist_name, 'Level1 Mini Series: Adventures at AMD')
        self.assertGreater(content.playlist_entry_count, 0)
