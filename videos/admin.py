from django.contrib import admin

from .models import Video, Comment, Playlist

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PlaylistAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Playlist Information', {'fields': ['title', 'uploader']}),
        ('Display Options', {'fields': ['thumbnail', 'listed']}),
        ('Videos', {'fields': ['videos']}),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

class VideoAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Video Information', {'fields': ['title', 'uploader', 'description', 'listed']}),
        ('Files', {'fields': ['video_file', 'thumbnail']}),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    inlines = [CommentInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

admin.site.register(Comment)
admin.site.register(Playlist)
admin.site.register(Video, VideoAdmin)