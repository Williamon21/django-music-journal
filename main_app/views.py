from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Album, Tag
from .forms import ListeningForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})


def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    listening_form = ListeningForm()
    return render(request, 'albums/detail.html', {
        'album': album,
        'listening_form': listening_form
    })


class AlbumCreate(CreateView):
    model = Album
    fields = '__all__'


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'year', 'rating', 'notes']


class AlbumDelete(DeleteView):
    model = Album
    success_url = '/albums/'


def add_listening(request, album_id):
    form = ListeningForm(request.POST)
    if form.is_valid():
        new_listening = form.save(commit=False)
        new_listening.album_id = album_id
        new_listening.save()
    return redirect('album-detail', album_id=album_id)


class TagCreate(CreateView):
    model = Tag
    fields = '__all__'


class TagList(ListView):
    model = Tag


class TagDetail(DetailView):
    model = Tag


class TagUpdate(UpdateView):
    model = Tag
    fields = ['name', 'color']


class TagDelete(DeleteView):
    model = Tag
    success_url = '/tags/'