from django.urls import path, re_path
from .views import Movies
from .views import Comments

urlpatterns = [
    path('movies', Movies.as_view(), name='movies'),
    path('comments', Comments.as_view(), name='comments'),
]
