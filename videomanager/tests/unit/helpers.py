from datetime import datetime

from django.utils.crypto import get_random_string

from videomanager.models import Channel, Playlist, Video


class ContentFactoryMixin:
    def setup_channel(
            self,
            channel_id: str = "",
            name: str = "",
            last_checked: datetime = None,
            monitored: bool = False,
    ):
        if channel_id == "":
            get_random_string(length=24)
        if name == "":
            name = "TestChannel-" + get_random_string(length=10)
        if last_checked is None:
            last_checked = datetime.now()

        channel = Channel(
            channel_id=channel_id,
            name=name,
            last_checked=last_checked,
            monitored=monitored,
            # avater
            # banner
        )
        channel.save()
        return channel

    def setup_playlist(
            self,
            playlist_id: str = "",
            channel=None,
            name: str = "",
            last_checked: datetime = None,
            monitored: bool = False,
            videos=None,
            # source
    ):
        if playlist_id == "":
            playlist_id = get_random_string(length=34)
        # if channel is None:
        #     channel = self.setup_channel()
        if name == "":
            name = "TestPlaylist-" + get_random_string(length=10)
        if last_checked is None:
            last_checked = datetime.now()
        if videos is None:
            videos = []

        playlist = Playlist(
            playlist_id=playlist_id,
            channel=channel,
            name=name,
            last_checked=last_checked,
            monitored=monitored,
        )
        playlist.save()
        for video in videos:
            playlist.videos.add(video)
        playlist.save()
        return playlist

    def setup_video(
            self,
            video_id: str = "",
            channel=None,
            title: str = "",
            # filename: str = "",
            description: str = "",
            upload_date: datetime = None,
            last_checked: datetime = None,
            monitored: bool = False,
            # file
    ):
        if video_id == "":
            video_id = get_random_string(length=11)
        if title == "":
            title = "TestVideo-" + get_random_string(length=10)
        if upload_date is None:
            upload_date = datetime.now()
        if last_checked is None:
            last_checked = datetime.now()
        video = Video(
            video_id=video_id,
            channel=channel,
            title=title,
            description=description,
            upload_date=upload_date,
            last_checked=last_checked,
            monitored=monitored,
        )
        video.save()
        return video
