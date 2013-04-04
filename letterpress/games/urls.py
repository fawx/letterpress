from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('letterpress.games.views',
    url(r'^$', 'list'),
    
    url(r'create/$', 'create'),

    url(r'api/$', 'api_game_list'),
    
    url(r'api/(?P<pk>\d+)', 'api_game_detail'),
)