from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "videomanager"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("c=<str:channel_id>/", views.channel, name="channel"),
    path("c=<str:channel_id>/p=<str:playlist_id>/", views.playlist, name="playlist"),
    path("c=<str:channel_id>/v=<str:video_id>/", views.video, name="video"),
    path("add/download/", views.download, name="download"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
