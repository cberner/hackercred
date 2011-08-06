from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackercred.views.home', name='home'),
    # url(r'^hackercred/', include('hackercred.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.index'),
    (r'^logout/$', 'app.views.logout'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^register/$', 'app.views.register'),
    (r'^user/(?P<id>[0-9]+)/$', 'app.views.view_user'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/home/christopher/Code/hackercred/src/hackercred/app/static'}),
    )