from rest_framework import serializers
from videomanager.models import Video, Playlist, Channel


class ChannelSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            'channel_id',
            'name',
            'profile_image',
        ]

    @staticmethod
    def get_profile_image(obj: Channel):
        if obj.profile_image:
            return obj.profile_image.url
        return None


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
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'video_id',
            'title',
            'upload_date',
            'channel',
            'thumbnail',
        ]

    @staticmethod
    def get_thumbnail(obj: Video):
        # Only return the relative path, e.g., "/media/thumbnails/example.jpg"
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
