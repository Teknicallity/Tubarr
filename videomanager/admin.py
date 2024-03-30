from django.contrib import admin
from .models import Channel, Playlist, Video

# Register your models here.
admin.site.register(Channel)
admin.site.register(Playlist)
admin.site.register(Video)