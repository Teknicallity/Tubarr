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

    class Meta:
        model = Playlist
        fields = [
            'playlist_id',
            'name',
            'channel',
        ]


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
