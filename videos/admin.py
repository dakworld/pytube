from django.contrib import admin

from .models import *

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class StreamCommentInline(admin.TabularInline):
    model = StreamComment
    extra = 1

class PodcastCommentInline(admin.TabularInline):
    model = PodcastComment
    extra = 1

class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 1

class PlaylistAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Playlist Information', {'fields': ['title', 'thumbnail', 'listed']}),
        ('Content', {'fields': ['videos', 'podcasts', 'streams']}),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    def get_queryset(self, request):
        qs = super(PlaylistAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

class SubscriptionManagerAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Information', {'fields': ['title']}),
        ('Email Messages', {'fields': ['template_subject', 'template_message']}),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    def get_queryset(self, request):
        qs = super(SubscriptionManagerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.emails = []
        obj.save()

class VideoAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Video Information', {'fields': ['title', 'description', 'listed']}),
        ('Files', {'fields': ['video_file', 'thumbnail']}),
        ('Subscription Managment', {'fields': ['subscription_manager']}),
    ]

    def get_queryset(self, request):
        qs = super(VideoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    inlines = [CommentInline, SubtitleInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
        for manager in obj.subscription_manager.all():
            manager.add_video_and_send_email(obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(VideoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['subscription_manager'].queryset = request.user.subscriptionmanager_set
        return form

class PodcastAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Podcast Information', {'fields': ['title', 'description', 'listed']}),
        ('Files', {'fields': ['audio_file', 'thumbnail']}),
        ('Subscription Managment', {'fields': ['subscription_manager']}),
    ]

    def get_queryset(self, request):
        qs = super(PodcastAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    inlines = [PodcastCommentInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
        for manager in obj.subscription_manager.all():
            manager.add_podcast_and_send_email(obj)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(PodcastAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['subscription_manager'].queryset = request.user.subscriptionmanager_set
        return form

class LiveStreamAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Video Information', {'fields': ['title', 'description', 'listed']}),
        ('stream Info', {'fields': ['stream_key', 'thumbnail']}),
        ('Subscription Managment', {'fields': ['subscription_manager']}),
    ]

    def get_queryset(self, request):
        qs = super(LiveStreamAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return True
    
    inlines = [StreamCommentInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
        for manager in obj.subscription_manager.all():
            manager.add_stream_and_send_email(obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(LiveStreamAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['subscription_manager'].queryset = request.user.subscriptionmanager_set
        return form

admin.site.register(SubscriptionManager, SubscriptionManagerAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(LiveStream, LiveStreamAdmin)
