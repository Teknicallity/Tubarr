from django.urls import path

from . import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view(), name='channel_list'),
    path('channels/<str:channel_id>', views.ChannelEntry.as_view(), name='channel_entry'),
    path('channels/<str:channel_id>/playlists/', views.PlaylistListForChannel.as_view(), name='channel_playlists'),
    path('channels/<str:channel_id>/videos/',    views.VideoListForChannel.as_view(), name='channel_videos'),
    path('playlists/', views.PlaylistList.as_view(), name='playlist_list'),
    path('playlists/<str:playlist_id>', views.PlaylistEntry.as_view(), name='playlist_entry'),
    path('videos/', views.VideoList.as_view(), name='video_list'),
    path('videos/<str:video_id>', views.VideoEntry.as_view(), name='video_entry'),
    path('search/', views.SearchApiView.as_view(), name='search'),
]