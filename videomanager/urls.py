from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "videomanager"
urlpatterns = [
    path("", views.index, name="index"),
    path("c=<str:channel_id>/", views.channel, name="channel"),
    path("c=<str:channel_id>/videos/", views.channel_videos, name="channel_videos"),
    path("c=<str:channel_id>/playlists/", views.channel_playlists, name="channel_playlists"),
    path("c=<str:channel_id>/v=<str:video_id>/", views.video, name="video"),
    path("c=<str:channel_id>/p=<str:playlist_id>/", views.playlist, name="playlist"),

    path("c=<str:channel_id>/delete/", views.delete_channel, name="delete_channel"),
    path("c=<str:channel_id>/v=<str:video_id>/delete/", views.delete_video, name="delete_video"),
    path("c=<str:channel_id>/p=<str:playlist_id>/delete/", views.delete_playlist, name="delete_playlist"),

    path("add/", views.add, name="add"),
    path("add/download/", views.download, name="download"),

    path('api/', include('videomanager.api.urls'), name='api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
