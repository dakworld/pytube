from django.urls import path

from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('stream/<int:pk>/', views.StreamView.as_view(), name='stream'),
    path('stream/<int:stream_id>/rate/', views.streamrate, name='streamrate'),
    path('stream/<int:stream_id>/comment/', views.streamcomment, name='streamcomment'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/register/', views.createuser, name='createuser'),
    path('subscribe/<int:pk>/', views.SubscriptionView.as_view(), name='subscribe'),
    path('subscribe/<int:pk>/subscribe/', views.subscribe, name='addsubscription'),
    path('users/<int:pk>/', views.UserView.as_view(), name='user'),
    path('playlists/<int:pk>/', views.PlaylistView.as_view(), name='playlist'),
    path('videos/<int:pk>/', views.VideoView.as_view(), name='video'),
    path('videos/<int:video_id>/rate/', views.rate, name='rate'),
    path('videos/<int:video_id>/comment/', views.comment, name='comment')
]
