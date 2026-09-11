from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, Song
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from slapify_project.forms import SongForm
from django.db.models import Q #for complex queries in the search function

# Create your views here.
def index(request):
    user_playlists = Playlist.objects.filter(user=request.user)

    context = {
        'user_playlists': user_playlists,
    }
    return render(request, 'index.html', context)

def my_playlists(request):
    user_playlists = Playlist.objects.filter(user=request.user)

    context = {
        'user_playlists': user_playlists,
    }
    return render(request, 'my_playlists.html', context)

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user.username  # Set artist to the username of the logged-in user
            song.save()
            return redirect('index')  # Redirect to home page after successful form submission
    else:
        form = SongForm()
    return render(request, 'slapify_web_app/add_song.html', {'form': form})

def edit_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SongForm(instance=song)
    return render(request, 'slapify_web_app/edit_song.html', {'form': form, 'song': song})

def user_songs(request):
    songs = Song.objects.filter(artist=request.user)
    return render(request, 'slapify_web_app/user_songs.html', {'songs': songs})

class PlaylistDetailView(generic.DetailView):
    """Lists songs in the playlist"""
    model = Playlist
    template_name = 'playlist_view.html'

    # allow the playlist detail page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    def get_queryset(self):
        return(
            Playlist.objects.filter(user=self.request.user)
        )

class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name']

    # redirect the user to index
    success_url = reverse_lazy('index')

    # allow the create page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    # set the 'user' attribute of Playlist to the logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeletePlaylistView(LoginRequiredMixin, DeleteView):
    model = Playlist

    # redirect the user to index
    success_url = reverse_lazy('index')

    # allow the delete page to have access to the user's playlists
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete_playlist", kwargs={"pk": self.object.pk})
            )

def remove_song(request, playlist_pk, song_pk):
    # Get the song and playlist objects
    song = get_object_or_404(Song, pk=song_pk)
    playlist = get_object_or_404(Playlist, pk=playlist_pk)

    playlist.songs.remove(song)

    return redirect('playlist_details', pk=playlist.pk)

def song_search(request):
    if request.method == "POST":
        # Get the input from the search bar
        searched = request.POST['searched']
        songs = Song.objects.filter(Q(title__icontains=searched) | 
                                    Q(genre__icontains=searched) | 
                                    Q(artist__icontains=searched))

        # return search results with the 'searched' input
        return render(request, 'slapify_web_app/song_search.html',
                      {'searched':searched,
                       'songs':songs}) 
    else:
        songs = Song.objects.all()
        return render(request, 'slapify_web_app/song_search.html',
                      {'songs':songs})

def add_song_to_playlist(request, song_pk):
    # Get the song object
    song = get_object_or_404(Song, pk=song_pk)
    user_playlists = Playlist.objects.filter(user=request.user)

    # Prevents a playlist from being displayed if it already has the song
    user_playlists_without_song = user_playlists.exclude(songs=song)

    context = {
        'song': song,
        'user_playlists': user_playlists_without_song,
    }
    return render(request, 'slapify_web_app/add_song_to_playlist.html', context)

def send_song_to_playlist(request, song_pk, playlist_pk):
    # Get the song and playlist objects
    song = get_object_or_404(Song, pk=song_pk)
    playlist = get_object_or_404(Playlist, pk=playlist_pk)

    playlist.songs.add(song)
    return redirect('song_search')

def AdminView(request):
    return render(request, 'admin/admin.html')

def genres(request):
    songs = Song.objects.filter()

    return render(request, 'admin/genres.html', {'songs':songs})

def songs(request):
    songs = Song.objects.filter()

    return render(request, 'admin/songs.html', {'songs':songs})