from django.conf.urls import patterns, include, url


urlpatterns = patterns('letterpress.games.views',
    url(r'^$', 'list'),
    
    url(r'create/$', 'create'),
)