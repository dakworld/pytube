from django.db import models
from django.contrib.postgres import fields as postgres_fields
from django.core import mail
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.FileField(upload_to='uploads/videos/profile_pics/')



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class SubscriptionManager(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    template_subject = models.CharField(max_length=50)
    template_message = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.created_by.username + ':' + self.title
    
    def send_mail(self, subject, body):
        mail.send_mail(subject, body, 'subscriptions@vidshare.net', [o.created_by.email for o in self.subscription_set.all()])

    def add_video_and_send_email(self, video):
        kwargs = {
            'name': self.title,
            'username': self.created_by.username,
            'title': video.title, 
            'content_type': 'video',
            'description': video.description, 
            'date': video.pub_date, 
            'url': 'https://vidshare.net/videos/'+str(video.id),
        }
        self.send_mail(self.template_subject.format(**kwargs), self.template_message.format(**kwargs))

    def add_blog_and_send_email(self, video):
        kwargs = {
            'name': self.title,
            'username': self.created_by.username,
            'title': video.title, 
            'content_type': 'blog post',
            'description': video.text, 
            'date': video.pub_date, 
            'url': 'https://vidshare.net/posts/'+str(video.id),
        }
        self.send_mail(self.template_subject.format(**kwargs), self.template_message.format(**kwargs))

    def add_podcast_and_send_email(self, video):
        kwargs = {
            'name': self.title,
            'username': self.created_by.username,
            'title': video.title, 
            'content_type': 'podcast',
            'description': video.description, 
            'date': video.pub_date, 
            'url': 'https://vidshare.net/podcasts/'+str(video.id),
        }
        self.send_mail(self.template_subject.format(**kwargs), self.template_message.format(**kwargs))

    def add_stream_and_send_email(self, video):
        kwargs = {
            'name': self.title,
            'username': self.created_by.username,
            'title': video.title, 
            'content_type': 'live stream',
            'description': video.description, 
            'date': video.pub_date, 
            'url': 'https://vidshare.net/stream/'+str(video.id),
        }
        self.send_mail(self.template_subject.format(**kwargs), self.template_message.format(**kwargs))

class Subscription(models.Model):
    subscription_manager = models.ForeignKey(SubscriptionManager, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subscription_manager.created_by.username + ':' + self.subscription_manager.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    subscription_manager = models.ManyToManyField(SubscriptionManager, blank=True)
    up_votes = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    video_file = models.FileField(upload_to='uploads/videos/')
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    listed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.created_by.username + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    subscription_manager = models.ManyToManyField(SubscriptionManager, blank=True)
    up_votes = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    listed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.created_by.username + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Podcast(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    subscription_manager = models.ManyToManyField(SubscriptionManager, blank=True)
    up_votes = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    audio_file = models.FileField(upload_to='uploads/videos/')
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    listed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.created_by.username + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class LiveStream(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    subscription_manager = models.ManyToManyField(SubscriptionManager, blank=True)
    up_votes = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    stream_key = models.CharField(max_length=50)
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    listed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.created_by.username + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Playlist(models.Model):
    title = models.CharField(max_length=100)
    listed = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to='uploads/videos/thumbnails/')
    videos = models.ManyToManyField(Video, blank=True)
    podcasts = models.ManyToManyField(Podcast, blank=True)
    streams = models.ManyToManyField(LiveStream, blank=True)
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

class StreamComment(models.Model):
    video = models.ForeignKey(LiveStream, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class BlogComment(models.Model):
    video = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class PodcastComment(models.Model):
    video = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class SubComment(models.Model):
    video = models.ForeignKey(LiveStream, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
