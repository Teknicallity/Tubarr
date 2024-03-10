import json

from django.conf import settings
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse

from .content import Content
from .models import Channel, Video, Playlist

# Create your views here.

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


# call this view through urls
def index(request):
    channel_list = Channel.objects.order_by("name")
    context = {"channel_list": channel_list}
    return render(request, "videomanager/channel_list.html", context)


def channel(request, channel_id):
    c = get_object_or_404(Channel, channel_id=channel_id)
    c_id = c.channel_id
    video_list = list(Video.objects.filter(channel__channel_id=c_id))
    playlist_list = list(Playlist.objects.filter(channel__channel_id=c_id))

    return render(request, "videomanager/channel.html", {"video_list": video_list, "playlist_list": playlist_list})


def playlist(request, playlist_id):
    p = get_object_or_404(Playlist, playlist_id=playlist_id)
    video_list = list(Video.objects.filter(playlists__playlist_id=p.playlist_id))
    # return HttpResponse("Playlist: %s" % playlist_id)
    return render(request, "videomanager/playlist.html", {"video_list": video_list})


def video(request, video_id):
    return HttpResponse("Video: %s" % video_id)


def add(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print('Posted url:', url)  # debug print
        content = Content(url)
        content.fill_info()

        request.session['url'] = url
        request.session['content'] = json.dumps(content.__dict__)
        info = content.get_info_dict()

        return JsonResponse({"url": url, "initial_info": info})

    return render(request, 'videomanager/add.html')


def download(request):
    if request.method == 'POST':
        url = request.session.get('url')
        content_json = request.session.get('content')

        # url = request.POST.get('url')

        if url and content_json:
            print('confirmed url:', url)  # debug print
            content_info = json.loads(content_json)
            content = Content(url)
            content.__dict__ = content_info

            content.download(settings.VIDEO_DIR, settings.CONFIG_DIR)

            del request.session['url']
            del request.session['content']

    # return HttpResponse("downloading")
    return HttpResponseRedirect(reverse('videomanager:add'))
