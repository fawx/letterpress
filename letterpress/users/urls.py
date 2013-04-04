from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout


urlpatterns = patterns('letterpress.users.views',
    url(r'login/$', login, { 'template_name': 'accounts/login.html' }),

    url(r'logout/$', logout, { 'next_page': '/' }),

    url(r'create/$', 'create'),
    
    url(r'create/success/$', 'create_success'),

    url(r'api/current/$', 'api_user_current'),
)
