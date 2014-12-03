from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from python_project_manager.settings import LOGIN_URL, LOGIN_REDIRECT_URL
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'new_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^new_project/$', 'project_manager.views.project_create'),
	url(r'^register/$', 'project_manager.views.register'),
	url(r'^login/$', 'project_manager.views.user_login'),
	url(r'^main/$', 'project_manager.views.main_page'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )