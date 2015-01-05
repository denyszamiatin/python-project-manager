from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from python_project_manager.settings import LOGIN_URL, LOGIN_REDIRECT_URL
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'project_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^new_project/$', 'project_manager.views.project_create'),
	url(r'^register/$', 'project_manager.views.register'),
	url(r'^login/$', 'project_manager.views.user_login'),
	url(r'^logout/$', 'project_manager.views.user_logout'),
	url(r'^main/$', 'project_manager.views.main_page'),
	url(r'^project/(?P<project_id>\d+)/$', 'project_manager.views.project'),
	url(r'^project/(?P<project_id>\d+)/add-user$', 'project_manager.views.add_user_to_project'),
	url(r'^project/(?P<id>\d+)/settings/$', 'project_manager.views.project_settings'),
	url(r'^project/(?P<id>\d+)/get_task_groups/$', 'project_manager.views.get_task_groups')

)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )