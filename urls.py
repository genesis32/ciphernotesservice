from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'keyserver/$', 'keyserver.views.index'),
    (r'keyserver/activate/(?P<activation_id>[0-9a-f]+)/$', 'keyserver.views.activate'), 
    # Examples:
    # url(r'^$', 'secdef.views.home', name='home'),
    # url(r'^secdef/', include('secdef.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
