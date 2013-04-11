from django.conf.urls import patterns, include, url


urlpatterns = patterns('letterpress.api.views',
    url(r'games/$', 'game_list'),
    
    url(r'games/(?P<pk>\d+)', 'game_detail'),
)