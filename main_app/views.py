from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Album, Tag, Song
from .forms import ListeningForm
from .services.spotify_api import search_spotify_albums, search_spotify_tracks


class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


@login_required
def album_index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'albums/index.html', {'albums': albums})


@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    listening_form = ListeningForm()

    tags_album_doesnt_have = Tag.objects.exclude(
        id__in=album.tags.all().values_list('id')
    )

    songs = Song.objects.filter(album=album)

    return render(request, 'albums/detail.html', {
        'album': album,
        'listening_form': listening_form,
        'tags': tags_album_doesnt_have,
        'songs': songs
    })


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'artist', 'year', 'rating', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['artist', 'year', 'rating', 'notes']


class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/albums/'


@login_required
def add_listening(request, album_id):
    form = ListeningForm(request.POST)

    if form.is_valid():
        new_listening = form.save(commit=False)
        new_listening.album_id = album_id
        new_listening.save()

    return redirect('album-detail', album_id=album_id)


@login_required
def associate_tag(request, album_id, tag_id):
    Album.objects.get(id=album_id).tags.add(tag_id)
    return redirect('album-detail', album_id=album_id)


@login_required
def remove_tag(request, album_id, tag_id):
    Album.objects.get(id=album_id).tags.remove(tag_id)
    return redirect('album-detail', album_id=album_id)


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = '__all__'


class TagList(LoginRequiredMixin, ListView):
    model = Tag


class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name', 'color']


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = '/tags/'


@login_required
def album_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = search_spotify_albums(query)

    return render(request, 'albums/search.html', {
        'query': query,
        'results': results
    })


@login_required
def spotify_import(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        year = request.POST.get('year')

        album = Album.objects.create(
            title=title,
            artist=artist,
            year=year,
            rating=0,
            notes='Imported from Spotify',
            user=request.user
        )

        return redirect('album-detail', album_id=album.id)

    return redirect('album-search')


@login_required
def song_search(request, album_id):
    album = Album.objects.get(id=album_id)
    query = request.GET.get('q', '')
    results = []

    if query:
        try:
            results = search_spotify_tracks(query)
        except Exception:
            results = []

    return render(request, 'albums/song_search.html', {
        'album': album,
        'query': query,
        'results': results
    })


@login_required
def spotify_song_import(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(id=album_id)

        title = request.POST.get('title')
        artist = request.POST.get('artist')
        spotify_id = request.POST.get('spotify_id')
        spotify_url = request.POST.get('spotify_url')
        preview_url = request.POST.get('preview_url')

        Song.objects.create(
            title=title,
            artist=artist,
            spotify_id=spotify_id,
            spotify_url=spotify_url,
            preview_url=preview_url,
            album=album
        )

        return redirect('album-detail', album_id=album_id)

    return redirect('album-detail', album_id=album_id)


def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('album-index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()

    return render(request, 'signup.html', {
        'form': form,
        'error_message': error_message
    })