from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    uploader = models.CharField(max_length=25)
    up_votes = models.IntegerField(default=0)
    video_file = models.FileField(upload_to='uploads/videos/')
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)