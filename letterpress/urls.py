from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'letterpress.views.home'),
    

    url(r'^games/', include('letterpress.games.urls')),


    url(r'^accounts/', include('letterpress.users.urls')),

    
    url(r'^api/', include('letterpress.api.urls')),


    url(r'^admin/', include(admin.site.urls)),
)
