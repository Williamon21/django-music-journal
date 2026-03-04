from django.shortcuts import render
from .models import Album

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    return render(request, 'albums/detail.html', {'album': album})