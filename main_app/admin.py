from django.contrib import admin
from .models import Album, Listening, Tag, Song

admin.site.register(Album)
admin.site.register(Listening)
admin.site.register(Tag)
admin.site.register(Song)