from django.db import models
from django.contrib import postgres
from django.core import mail
from django.contrib.auth.models import User

class SubscriptionManager(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    emails = postgres.fields.ArrayField(models.EmailField(max_length=60))
    template_subject = models.CharField(max_length=50)
    template_message = models.TextField(max_length=1000)
    def __str__(self):
        return self.created_by.username + ':' + self.title
    def send_mail(self, subject, body):
        mail.send_mail(subject, body, str(self.created_by.username) + '@pytube.localhost', list(self.emails))
    def add_video_and_send_email(self, video):
        kwargs = {
            'name': self.title,
            'username': self.created_by.username,
            'title': video.title, 
            'description': video.description, 
            'date': video.pub_date, 
            'url': '/videos/'+str(video.id),
        }
        self.send_mail(self.template_subject.format(**kwargs), self.template_message.format(**kwargs))

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    uploader = models.CharField(max_length=25)
    subscription_manager = models.ManyToManyField(SubscriptionManager)
    up_votes = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    video_file = models.FileField(upload_to='uploads/videos/')
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    listed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.uploader + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Playlist(models.Model):
    title = models.CharField(max_length=100)
    uploader = models.CharField(max_length=25)
    listed = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    videos = models.ManyToManyField(Video)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Subtitle(models.Model):
    subtitle_file = models.FileField(upload_to='uploads/videos/subtitles/')
    language = models.CharField(max_length=5)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)