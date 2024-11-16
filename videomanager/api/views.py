import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from videomanager.models import Channel, Video, Playlist
from .serializers import VideoSerializer, PlaylistSerializer, ChannelSerializer
from ..utils.search import search

logger = logging.getLogger(__name__)


class ChannelList(generics.ListAPIView):
    queryset = Channel.objects.all().order_by('name')
    serializer_class = ChannelSerializer


class ChannelEntry(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'channel_id'


class PlaylistList(generics.ListAPIView):
    queryset = Playlist.objects.all().order_by('name')
    serializer_class = PlaylistSerializer


class PlaylistListForChannel(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        c = get_object_or_404(Channel, channel_id=channel_id)
        return Playlist.objects.filter(channel=c)


class PlaylistEntry(generics.RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'playlist_id'


class VideoList(generics.ListAPIView):
    # def get(self, request):
    #     # search = request.GET.get('search')
    #     video_list = Video.objects.filter(status=Video.STATUS.DOWNLOADED)
    #     serializer = VideoSerializer(video_list, many=True)
    #     return Response(serializer.data)
    queryset = Video.objects.filter(status=Video.STATUS.DOWNLOADED).order_by('-upload_date')
    serializer_class = VideoSerializer


class VideoListForChannel(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        c = get_object_or_404(Channel, channel_id=channel_id)
        return Video.objects.filter(channel=c, status=Video.STATUS.DOWNLOADED).order_by('-upload_date')


class VideoEntry(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'video_id'


class SearchApiView(APIView):
    DEFAULT_AMOUNT = 3
    MAX_AMOUNT = 100
    DEFAULT_TYPE = 'all'
    ALLOWED_TYPES = {'all', 'videos', 'playlists', 'channels'}

    def get(self, request):
        search_query = request.GET.get('q') or request.GET.get('query')
        search_size = min(self.MAX_AMOUNT, int(request.GET.get('size', self.DEFAULT_AMOUNT)))
        search_type = request.GET.get('type', self.DEFAULT_TYPE)

        if search_type not in self.ALLOWED_TYPES:
            return Response(
                {'error': f'Invalid search type: {search_type}. Allowed values are {", ".join(self.ALLOWED_TYPES)}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = search(search_query=search_query, amount=search_size, search_type=search_type)
        return Response(data=results, status=status.HTTP_200_OK)


class DownloadingVideos(APIView):

    @staticmethod
    def get(request):
        queued_videos_list = Video.objects.filter(status=Video.STATUS.QUEUED)
        errored_videos_list = Video.objects.filter(status=Video.STATUS.ERRORED)

        return Response(
            data={
                'queued_videos': VideoSerializer(queued_videos_list, many=True).data,
                'errored_videos': VideoSerializer(errored_videos_list, many=True).data
            },
            status=status.HTTP_200_OK
        )


class DownloadingVideosCount(APIView):
    @staticmethod
    def get(request):
        queued_videos_count = Video.objects.filter(status=Video.STATUS.QUEUED).count()
        errored_videos_count = Video.objects.filter(status=Video.STATUS.ERRORED).count()

        return Response(
            data={
                'queued_videos_count': queued_videos_count,
                'errored_videos_count': errored_videos_count
            },
            status=status.HTTP_200_OK
        )
