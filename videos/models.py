from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    uploader = models.CharField(max_length=25)
    up_votes = models.IntegerField(default=0)
    video_file = models.FileField(upload_to='uploads/videos/')
    pub_date = models.DateTimeField('date published')
    comments = []
    def __str__(self):
        return self.uploader + ':' + self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    email = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.name + '::' + str(self.pub_date)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)