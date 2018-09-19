from django.urls import path, re_path
from . import views

urlpatterns = [
    path('movies', views.movies, name='movies'),
    path('comments', views.comments, name='comments'),
]
