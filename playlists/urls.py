from django.urls import path 
from .views import playlists_view

urlpatterns = [
    path('', playlists_view, name='playlists'),
]