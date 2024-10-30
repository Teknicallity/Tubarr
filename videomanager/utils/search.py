from videomanager.models import Channel, Video, Playlist
from ..api.serializers import VideoSerializer, PlaylistSerializer, ChannelSerializer


def search(search_query, amount: int, search_type='all'):
    if search_type == 'videos':
        video_results = Video.objects.filter(title__icontains=search_query, status=Video.STATUS.DOWNLOADED)[:amount]
        return {'videos': VideoSerializer(video_results, many=True).data}
    if search_type == 'playlists':
        playlist_results = Playlist.objects.filter(name__icontains=search_query)[:amount]
        return {'playlists': PlaylistSerializer(playlist_results, many=True).data}
    if search_type == 'channels':
        channel_results = Channel.objects.filter(name__icontains=search_query)[:amount]
        return {'channels': ChannelSerializer(channel_results, many=True).data}
    else:
        video_results = Video.objects.filter(title__icontains=search_query, status=Video.STATUS.DOWNLOADED)[:amount]
        playlist_results = Playlist.objects.filter(name__icontains=search_query)[:amount]
        channel_results = Channel.objects.filter(name__icontains=search_query)[:amount]

        return {
            'videos': VideoSerializer(video_results, many=True).data,
            'playlists': PlaylistSerializer(playlist_results, many=True).data,
            'channels': ChannelSerializer(channel_results, many=True).data
        }
