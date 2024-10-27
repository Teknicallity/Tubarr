import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import DeleteView

from videomanager.content_handlers.content_factory import ContentFactory, UnknownContentTypeError, UnknownUrlError
from .models import Channel, Video, Playlist

logger = logging.getLogger(__name__)


# Create your views here.

# call this view through urls
def index(request):
    channel_list = Channel.objects.order_by("name")
    context = {"channel_list": channel_list}
    return render(request, "videomanager/channel_list.html", context)


def channel(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    c_id = c.channel_id
    video_list = list(Video.objects.filter(channel__channel_id=c_id, status=Video.STATUS.DOWNLOADED))
    playlist_list = list(Playlist.objects.filter(channel__channel_id=c_id))

    return render(
        request,
        "videomanager/channel_home.html",
        {"channel": c, "video_list": video_list, "playlist_list": playlist_list}
    )


def playlist(request, channel_id, playlist_id):
    p = get_object_or_404(Playlist, playlist_id=playlist_id)
    video_list = list(Video.objects.filter(playlists__playlist_id=p.playlist_id))
    # return HttpResponse("Playlist: %s" % playlist_id)
    return render(request, "videomanager/playlist.html", {"video_list": video_list})


def video(request, channel_id, video_id):
    v = get_object_or_404(Video, video_id=video_id)
    # url = settings.MEDIA_URL + v.channel.channel_id + '/' + v.filename
    # returns /content/... which results in /channels//content/...

    url = 'content/' + v.channel.channel_id + '/' + v.filename
    logger.debug(f'Video location url: {url}')
    return render(request, "videomanager/video.html", {"video": v, "video_url": url})


def add(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        err = ''
        attribute_dictionary = ''

        content = ContentFactory.get_content_object(url)
        try:
            content.fill_info()
        except UnknownContentTypeError:
            err = "Could not identify Youtube content type"
        except UnknownUrlError:
            err = "Not a Youtube Url"
        else:
            attribute_dictionary = content.get_attribute_dict()
            request.session['url'] = url
        return JsonResponse({"url": url, "initial_info": attribute_dictionary, "error": err})

    return render(request, 'videomanager/add.html')


def download(request):
    if request.method == 'POST':
        url = request.session.get('url')
        if url:
            logger.debug(f'Starting url download: {url}')
            content = ContentFactory.get_content_object(url)
            content.fill_info()
            content.download()

        del request.session['url']

    # return HttpResponse("downloading")
    return HttpResponseRedirect(reverse('videomanager:add'))


def delete_channel(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    if request.method == "GET":
        context = {'delete_url': reverse('videomanager:delete_channel', args=(c.channel_id,))}
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        c.delete()
        return HttpResponseRedirect(reverse('videomanager:index'))


def delete_playlist(request, channel_id, playlist_id):
    p = get_object_or_404(Playlist, playlist_id=playlist_id)
    if request.method == "GET":
        context = {'delete_url': reverse('videomanager:delete_playlist', args=(p.channel.channel_id, p.playlist_id,))}
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        p.delete()
        if p.channel.is_empty():
            p.channel.delete()
            return HttpResponseRedirect(reverse('videomanager:index'))
        return HttpResponseRedirect(reverse('videomanager:channel', args=(p.channel.channel_id,)))


def delete_video(request, channel_id, video_id):
    v = get_object_or_404(Video, video_id=video_id)
    if request.method == "GET":
        context = {'delete_url': reverse('videomanager:delete_video', args=(v.channel.channel_id, v.video_id,))}
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        v.delete()
        if v.channel.is_empty():
            v.channel.delete()
            return HttpResponseRedirect(reverse('videomanager:index'))
        return HttpResponseRedirect(reverse('videomanager:channel', args=(v.channel.channel_id,)))
