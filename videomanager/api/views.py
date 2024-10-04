import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import DeleteView
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from videomanager.content_handlers.content_factory import ContentFactory, UnknownContentTypeError, UnknownUrlError
from videomanager.models import Channel, Video, Playlist
from .serializers import VideoSerializer, PlaylistSerializer, ChannelSerializer

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
    serializer_class = VideoSerializer


class PlaylistListForChannel(APIView):
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
