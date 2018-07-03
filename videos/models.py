from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    uploader = models.CharField(max_length=25)
    up_votes = models.IntegerField(default=0)
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

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)