from django.urls import path

from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:video_id>/', views.video, name='video')
]