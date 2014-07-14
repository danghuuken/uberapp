from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'muni_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','source.views.index'),
    #url(r'^(?P<slug>[\w\-]+)/$','source.views.post')
    url(r'^stoplist/(?P<tag>[0-9a-zA-Z]+)/','source.views.stoplist'),
    url(r'^stoplist/','source.views.stoplist', name='stop_list'),
    url(r'^departures/(?P<tag>[A-Z0-9]+)/$','source.views.departures', name='stop_departures'),
    url(r'^departures/','source.views.departures', name='stop_departure'),
)
