from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

hp = "[0-9A-Z]"
ipad_guid = '%s{8}\-%s{4}\-%s{4}\-%s{4}\-%s{12})/$' % (hp, hp, hp, hp, hp)
urlpatterns = patterns('',
    (r'keyserver/$', 'keyserver.views.index'),
    (r'keyserver/activate/(?P<activation_id>[0-9a-f]+)/$', 'keyserver.views.activate'), 
    (r'keyserver/registered/(?P<udid>%s' % (ipad_guid), 'keyserver.views.registered'),
    # Examples:
    # url(r'^$', 'secdef.views.home', name='home'),
    # url(r'^secdef/', include('secdef.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
