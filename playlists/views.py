from django.shortcuts import render

from playlists.codes import youtube_api_oauth_to_access_user_accounts as yu_oauth
from playlists.codes import youtube_api_playlist_sort_by_popular as yu_pl_popular
from playlists.codes import youtube_api_playlist_length as yu_pl_length


def playlists_view(request):
    context = {'error_': 'not a valid link'}
    if(request.GET.get('length')):
        link = str(request.GET.get('playlist_link'))
        if 'list' not in link:
            context = {'error': 'not a valid link'} 
            return render(request, 'playlists/playlist.html', context)
        try:
            context = yu_pl_length.length(link)
        except:
            context = {'error': 'not a valid link'} 
    
    if(request.GET.get('popular')):
        link = str(request.GET.get('playlist_link'))
        if 'list' not in link:
            context = {'error': 'not a valid link'} 
            return render(request, 'playlists/playlist.html', context)
        try:
            context = yu_pl_popular.sortByPopularity(link)
        except:
            context = {'error': 'not a valid link'} 
    
    if(request.GET.get('private')):
        try:
            context = yu_oauth.privateData()
        except:
            context = {'error': 'not a valid link'}

    return render(request, 'playlists/playlist.html', context)