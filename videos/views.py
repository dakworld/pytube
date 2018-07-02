from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.postgres.search import TrigramDistance

from .models import Video, Comment

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
        search = Video.objects.extra({'title_text': "CAST(title as text)"}).annotate(distance=TrigramDistance('title_text', query),).filter(distance__lte=0.7).order_by('distance')
        return search

class VideoView(generic.DetailView):
    model = Video
    template_name = 'videos/video.html'

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
    video.comment_set.create(name = request.POST['name'], email = '', message = request.POST['comment_text'], pub_date=timezone.now())
    video.save()
    return HttpResponseRedirect(reverse('videos:video', args=(video.id,)))