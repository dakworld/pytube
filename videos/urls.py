from django.urls import path

from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/register/', views.createuser, name='createuser'),
    path('users/<int:pk>/', views.UserView.as_view(), name='user'),
    path('playlists/<int:pk>/', views.PlaylistView.as_view(), name='playlist'),
    path('videos/<int:pk>/', views.VideoView.as_view(), name='video'),
    path('videos/<int:video_id>/rate/', views.rate, name='rate'),
    path('videos/<int:video_id>/comment/', views.comment, name='comment')
]