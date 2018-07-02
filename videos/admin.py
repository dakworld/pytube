from django.contrib import admin

from .models import Video, Comment

admin.site.register(Comment)
admin.site.register(Video)