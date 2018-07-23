from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models.functions import Greatest
from django.db.models import Max, Min, F
from django.contrib.postgres.search import TrigramSimilarity
from itertools import chain
from django.contrib.auth.models import User, Group

from .models import *

class IndexView(generic.ListView):
    template_name = 'videos/index.html'
    context_object_name = 'best_videos_list'
    paginate_by = 20

    def get_queryset(self):
        streams = LiveStream.objects.annotate(order=F('views') * F('up_votes'))
        videos = Video.objects.annotate(order=F('views') * F('up_votes'))
        playlists = Playlist.objects.annotate(order=Min('videos__views') * Max('videos__up_votes'))
        podcasts = Podcast.objects.annotate(order=F('views') * F('up_votes'))
        #users = User.objects.annotate(order=Max(Count('subscription_manager__emails')))
        return sorted(chain(podcasts, playlists, videos, streams), key=lambda instance: instance.order, reverse=True)

class SearchView(generic.ListView):
    template_name = 'videos/index.html'
    context_object_name = 'best_videos_list'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET['search']
        videos = Video.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('created_by__username', query),
            TrigramSimilarity('description', query),
            Max(TrigramSimilarity('comment__message', query))
            ))
        podcasts = Podcast.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('created_by__username', query),
            TrigramSimilarity('description', query),
            Max(TrigramSimilarity('podcastcomment__message', query))
            ))
        streams = LiveStream.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('created_by__username', query),
            TrigramSimilarity('description', query),
            Max(TrigramSimilarity('streamcomment__message', query))
            ))
        playlists = Playlist.objects.annotate(similarity=Greatest(
            TrigramSimilarity('title', query), 
            TrigramSimilarity('created_by__username', query),
            Max(TrigramSimilarity('videos__title', query))
            ))
        users = User.objects.annotate(similarity=Greatest(
            TrigramSimilarity('username', query), 
            TrigramSimilarity('email', query),
            Max(TrigramSimilarity('video__title', query)),
            Max(TrigramSimilarity('playlist__title', query))
            ))
        search = sorted(chain(videos, streams, podcasts, playlists, users), key=lambda instance: instance.similarity, reverse=True)
        return search

class VideoView(generic.DetailView):
    model = Video
    template_name = 'videos/video.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save()
        return context

class PodcastView(generic.DetailView):
    model = Podcast
    template_name = 'videos/podcast.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save()
        return context

class PlaylistView(generic.DetailView):
    model = Playlist
    template_name = 'videos/playlist.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        streams = obj.streams.annotate(order=F('views') * F('up_votes'))
        videos = obj.videos.annotate(order=F('views') * F('up_votes'))
        podcasts = obj.podcasts.annotate(order=F('views') * F('up_votes'))
        context['best_videos_list'] = sorted(chain(videos, streams, podcasts), key=lambda instance: instance.order, reverse=True)
        return context


class UserView(generic.DetailView):
    model = User
    template_name = 'videos/user.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        streams = obj.livestream_set.annotate(order=F('views') * F('up_votes'))
        videos = obj.video_set.annotate(order=F('views') * F('up_votes'))
        podcasts = obj.podcast_set.annotate(order=F('views') * F('up_votes'))
        playlists = obj.playlist_set.annotate(order=Min('videos__views') * Max('videos__up_votes'))
        context['best_videos_list'] = sorted(chain(videos, streams, podcasts, playlists), key=lambda instance: instance.order, reverse=True)
        return context

class StreamView(generic.DetailView):
    model = LiveStream
    template_name = 'videos/livestream.html'
    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save()
        return context

class SubscriptionView(generic.DetailView):
    model = SubscriptionManager
    template_name = 'videos/subscribe.html'

class RegisterView(generic.TemplateView):
	template_name = 'videos/register.html'

def subscribe(request, pk):
    subscription = get_object_or_404(SubscriptionManager, pk=pk)
    subscription.emails.append(request.POST['email'])
    subscription.save()
    return HttpResponseRedirect(reverse('videos:user', args=(subscription.created_by.id,)))

def rate(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.POST['choice'] == 'up':
        video.up_votes += 1
        video.save()
    elif request.POST['choice'] == 'down':
        if video.up_votes >= 1:
            video.up_votes -= 1
            video.save()
    return HttpResponseRedirect(reverse('videos:video', args=(video.id,)))

def comment(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.comment_set.create(name = request.POST['name'], message = request.POST['comment_text'])
    video.save()
    return HttpResponseRedirect(reverse('videos:video', args=(video.id,)))

def streamrate(request, stream_id):
    video = get_object_or_404(LiveStream, pk=stream_id)
    if request.POST['choice'] == 'up':
        video.up_votes += 1
        video.save()
    elif request.POST['choice'] == 'down':
        if video.up_votes >= 1:
            video.up_votes -= 1
            video.save()
    return HttpResponseRedirect(reverse('videos:stream', args=(video.id,)))

def streamcomment(request, stream_id):
    video = get_object_or_404(LiveStream, pk=stream_id)
    video.streamcomment_set.create(name = request.POST['name'], message = request.POST['comment_text'])
    video.save()
    return HttpResponseRedirect(reverse('videos:stream', args=(video.id,)))

def podcastrate(request, podcast_id):
    video = get_object_or_404(Podcast, pk=podcast_id)
    if request.POST['choice'] == 'up':
        video.up_votes += 1
        video.save()
    elif request.POST['choice'] == 'down':
        if video.up_votes >= 1:
            video.up_votes -= 1
            video.save()
    return HttpResponseRedirect(reverse('videos:podcast', args=(video.id,)))

def podcastcomment(request, podcast_id):
    video = get_object_or_404(Podcast, pk=podcast_id)
    video.podcastcomment_set.create(name = request.POST['name'], message = request.POST['comment_text'])
    video.save()
    return HttpResponseRedirect(reverse('videos:podcast', args=(video.id,)))

def createuser(request):
    user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
    user.is_staff = True 
    user.save()
    my_group = Group.objects.get(name='creator') 
    my_group.user_set.add(user)
    return HttpResponseRedirect('/admin')
