from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models.functions import Greatest
from django.db.models import Max
from django.contrib.postgres.search import TrigramSimilarity
from itertools import chain
from django.contrib.auth.models import User, Group

from .models import Video, Comment, Playlist

class IndexView(generic.ListView):
    template_name = 'videos/index.html'
    context_object_name = 'best_videos_list'
    paginate_by = 20

    def get_queryset(self):
        return Video.objects.order_by('-up_votes')

class SearchView(generic.ListView):
    template_name = 'videos/index.html'
    context_object_name = 'best_videos_list'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET['search']
        videos = Video.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('uploader', query),
            TrigramSimilarity('description', query),
            Max(TrigramSimilarity('comment__message', query))
            )).order_by('-similarity')
        playlists = Playlist.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('uploader', query),
            Max(TrigramSimilarity('videos__title', query))
            )).order_by('-similarity')
        search = list(chain(videos, playlists))
        return search

class VideoView(generic.DetailView):
    model = Video
    template_name = 'videos/video.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        self.get_object().views += 1
        return context

class PlaylistView(generic.DetailView):
    model = Playlist
    template_name = 'videos/playlist.html'

class RegisterView(generic.TemplateView):
	template_name = 'videos/register.html'

def rate(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.POST['choice'] == 'up':
        video.up_votes += 1
        video.save()
    elif request.POST['choice'] == 'down':
        video.up_votes -= 1
        video.save()
    return HttpResponseRedirect(reverse('videos:video', args=(video.id,)))

def comment(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.comment_set.create(name = request.POST['name'], message = request.POST['comment_text'])
    video.save()
    return HttpResponseRedirect(reverse('videos:video', args=(video.id,)))

def createuser(request):
    user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
    user.is_staff = True 
    user.save()
    my_group = Group.objects.get(name='creator') 
    my_group.user_set.add(user)
    return HttpResponseRedirect('/admin')