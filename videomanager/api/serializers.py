from rest_framework import serializers
from videomanager.models import Video, Playlist, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'channel_id',
            'name',
            'profile_image',
        ]


class PlaylistSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            'playlist_id',
            'name',
            'channel',
            'thumbnail',
        ]

    @staticmethod
    def get_thumbnail(obj: Playlist):
        first_video = obj.videos.first()
        return first_video.thumbnail.url if first_video else None


class VideoSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()

    class Meta:
        model = Video
        fields = [
            'video_id',
            'title',
            'upload_date',
            'channel',
            'thumbnail',
        ]
