from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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
)
