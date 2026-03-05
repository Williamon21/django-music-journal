from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


class AlbumCreate(CreateView):
    model = Album
    fields = '__all__'


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'year', 'rating', 'notes']  # change if needed


class AlbumDelete(DeleteView):
    model = Album
    success_url = '/albums/'