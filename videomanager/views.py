import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from videomanager.content_handlers.content_factory import ContentFactory, UnknownContentTypeError, UnknownUrlError
from .models import Channel, Video, Playlist
from .utils.search import search

logger = logging.getLogger(__name__)


# Create your views here.

# call this view through urls
def index(request):
    channel_list = Channel.objects.order_by("name")
    context = {'DEMO_MODE': settings.DEMO_MODE, "channel_list": channel_list}
    return render(request, "videomanager/channel_list.html", context)


def channel(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    c_id = c.channel_id
    video_list = list(Video.objects.filter(channel__channel_id=c_id, status=Video.STATUS.DOWNLOADED))
    playlist_list = list(Playlist.objects.filter(channel__channel_id=c_id))

    return render(
        request,
        "videomanager/channel_home.html",
        {'DEMO_MODE': settings.DEMO_MODE, "channel": c, "video_list": video_list, "playlist_list": playlist_list}
    )


def channel_videos(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    c_id = c.channel_id
    video_list = list(Video.objects.filter(channel__channel_id=c_id, status=Video.STATUS.DOWNLOADED))
    return render(
        request,
        "videomanager/channel_videos.html",
        {'DEMO_MODE': settings.DEMO_MODE, "channel": c, "video_list": video_list}
    )


def all_videos(request):
    v = list(Video.objects.all())
    return render(
        request,
        "videomanager/all_videos.html",
        {'DEMO_MODE': settings.DEMO_MODE, "video_list": v}
    )


def channel_playlists(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    c_id = c.channel_id
    playlist_list = list(Playlist.objects.filter(channel__channel_id=c_id))
    return render(
        request,
        "videomanager/channel_playlists.html",
        {'DEMO_MODE': settings.DEMO_MODE, "channel": c, "playlist_list": playlist_list}
    )


def playlist(request, channel_id, playlist_id):
    p = get_object_or_404(Playlist, playlist_id=playlist_id)
    video_list = list(Video.objects.filter(playlists__playlist_id=p.playlist_id))
    # return HttpResponse("Playlist: %s" % playlist_id)
    return render(
        request,
        "videomanager/playlist.html",
        {
            'DEMO_MODE': settings.DEMO_MODE,
            "playlist": p,
            "video_list": video_list,
        }
    )


def video(request, channel_id, video_id):
    v = get_object_or_404(Video, video_id=video_id)
    # url = settings.MEDIA_URL + v.channel.channel_id + '/' + v.filename
    # returns /content/... which results in /channels//content/...

    url = 'content/' + v.channel.channel_id + '/' + v.filename
    logger.debug(f'Video location url: {url}')
    return render(
        request,
        "videomanager/video.html",
        {
            'DEMO_MODE': settings.DEMO_MODE,
            "video": v,
            "video_url": url
        }
    )


def add(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        err = ''
        attribute_dictionary = ''

        logger.info(f'Requested url: {url}')

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

    return render(request, 'videomanager/add.html', {'DEMO_MODE': settings.DEMO_MODE})


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
    if settings.DEMO_MODE:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    c = get_object_or_404(Channel, channel_id=channel_id)
    if request.method == "GET":
        context = {'delete_url': reverse('videomanager:delete_channel', args=(c.channel_id,))}
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        c.delete()
        return HttpResponseRedirect(reverse('videomanager:index'))


def delete_playlist(request, channel_id, playlist_id):
    if settings.DEMO_MODE:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    p = get_object_or_404(Playlist, playlist_id=playlist_id)
    if request.method == "GET":
        context = {
            'DEMO_MODE': settings.DEMO_MODE,
            'delete_url': reverse('videomanager:delete_playlist', args=(p.channel.channel_id, p.playlist_id,))
        }
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        p.delete()
        if p.channel.is_empty():
            p.channel.delete()
            return HttpResponseRedirect(reverse('videomanager:index'))
        return HttpResponseRedirect(reverse('videomanager:channel', args=(p.channel.channel_id,)))


def delete_video(request, channel_id, video_id):
    if settings.DEMO_MODE:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    v = get_object_or_404(Video, video_id=video_id)
    if request.method == "GET":
        context = {
            'DEMO_MODE': settings.DEMO_MODE,
            'delete_url': reverse('videomanager:delete_video', args=(v.channel.channel_id, v.video_id,))
        }
        return render(request, 'videomanager/delete_redirect.html', context)

    if request.method == "POST":
        v.delete()
        if v.channel.is_empty():
            v.channel.delete()
            return HttpResponseRedirect(reverse('videomanager:index'))
        return HttpResponseRedirect(reverse('videomanager:channel', args=(v.channel.channel_id,)))


def search_view(request):
    DEFAULT_AMOUNT = 10
    MAX_AMOUNT = 100
    DEFAULT_TYPE = 'all'
    ALLOWED_TYPES = {'all', 'videos', 'playlists', 'channels'}

    search_query = request.GET.get('q') or request.GET.get('query')
    search_size = min(MAX_AMOUNT, int(request.GET.get('size', DEFAULT_AMOUNT)))
    search_type = request.GET.get('type', DEFAULT_TYPE)

    if search_query == '':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # if search_type not in ALLOWED_TYPES:
    #     return Response(
    #         {'error': f'Invalid search type: {search_type}. Allowed values are {", ".join(ALLOWED_TYPES)}.'},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    results = search(search_query, search_size, search_type)
    return render(
        request,
        'videomanager/search.html',
        {'DEMO_MODE': settings.DEMO_MODE, 'results': results}
    )


def queued_list(request):
    queued_videos = list(Video.objects.filter(status=Video.STATUS.QUEUED))
    errored_videos = list(Video.objects.filter(status=Video.STATUS.ERRORED))
    v = Video.objects.first()

    return render(
        request,
        'videomanager/queued_list.html',
        {'DEMO_MODE': settings.DEMO_MODE, 'queued_videos': queued_videos, 'errored_videos': errored_videos}
    )
