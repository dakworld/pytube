from django.urls import path

from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/<dtype>/', views.ClassView.as_view(), name='class'),
    path('stream/<int:pk>/', views.StreamView.as_view(), name='stream'),
    path('stream/<int:stream_id>/rate/', views.streamrate, name='streamrate'),
    path('stream/<int:stream_id>/comment/', views.streamcomment, name='streamcomment'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/register/', views.createuser, name='createuser'),
    path('subscribe/<int:pk>/', views.subscribe, name='subscribe'),
    path('subscribe/<int:pk>/subscribe/', views.subscribe, name='addsubscription'),
    path('users/<int:pk>/', views.UserView.as_view(), name='user'),
    path('users/<int:pk>/specs/', views.UserSpecView.as_view(), name='userspec'),
    path('playlists/<int:pk>/', views.PlaylistView.as_view(), name='playlist'),
    path('videos/<int:pk>/', views.VideoView.as_view(), name='video'),
    path('videos/<int:video_id>/rate/', views.rate, name='rate'),
    path('videos/<int:video_id>/comment/', views.comment, name='comment'),
    path('podcasts/<int:pk>/', views.PodcastView.as_view(), name='podcast'),
    path('podcasts/<int:podcast_id>/rate/', views.podcastrate, name='podcastrate'),
    path('podcasts/<int:podcast_id>/comment/', views.podcastcomment, name='podcastcomment'),
    path('post/<int:pk>/', views.BlogView.as_view(), name='post'),
    path('post/<int:blog_id>/rate/', views.blograte, name='postrate'),
    path('post/<int:blog_id>/comment/', views.blogcomment, name='postcomment'),
]
