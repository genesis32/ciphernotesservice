from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

hp = "[0-9A-Z]"
udid = '(?P<udid>%s{8}\-%s{4}\-%s{4}\-%s{4}\-%s{12})' % (hp, hp, hp, hp, hp)
urlpatterns = patterns('',
    (r'keyserver/$', 'keyserver.views.index'),
    (r'keyserver/activate/' + udid + '/$' , 'keyserver.views.activate'), 
    (r'keyserver/activated/' + udid + '/$', 'keyserver.views.activated'),
    (r'keyserver/get/pubkey/(?P<uid>\d+)/$', 'keyserver.views.getpubkey'),
    (r'keyserver/send/message/(?P<toid>\d+)/$', 'keyserver.views.sendmessage'),
    # Examples
    # url(r'^$', 'secdef.views.home', name='home'),
    # url(r'^secdef/', include('secdef.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
