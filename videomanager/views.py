from datetime import datetime
import json

from django.conf import settings
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .content import Content, UnknownContentTypeError, UnknownUrlError
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


def video(request, video_id, channel_id):
    v = get_object_or_404(Video, video_id=video_id)
    # url = settings.MEDIA_URL + v.channel.channel_id + '/' + v.filename
    # returns /content/... which results in /channels//content/...

    url = 'content/' + v.channel.channel_id + '/' + v.filename
    print("url", url)
    return render(request, "videomanager/video.html", {"video": v, "video_url": url})


def add(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        err = ''

        content = Content(url)
        try:
            content.fill_info()
        except UnknownContentTypeError:
            err = "Could not identify Youtube content type"
        except UnknownUrlError:
            err = "Not a Youtube Url"
        else:
            request.session['url'] = url
            request.session['content'] = json.dumps(content.__dict__)

        info = content.get_info_dict()

        return JsonResponse({"url": url, "initial_info": info, "error": err})

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

            content.download(settings.MEDIA_ROOT, settings.CONFIG_DIR)

            if content.downloaded:
                channel_entry, created = Channel.objects.get_or_create(
                    channel_id=content.channel_id,
                    defaults={
                        'name': content.channel_name,
                        'last_checked': timezone.now()
                    }
                )

                channel_entry.video_set.create(
                    video_id=content.video_id,
                    title=content.video_title,
                    filename=content.filename,
                    description=content.video_description,
                    upload_date=datetime.strptime(content.upload_date, "%Y%m%d").date(),
                    last_checked=timezone.now()
                )

        del request.session['url']
        del request.session['content']

    # return HttpResponse("downloading")
    return HttpResponseRedirect(reverse('videomanager:add'))
