from django.urls import path

from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<int:pk>/', views.VideoView.as_view(), name='video'),
    path('<int:video_id>/rate/', views.rate, name='rate'),
    path('<int:video_id>/comment/', views.comment, name='comment')
]