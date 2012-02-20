from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'keyserver/$', 'web.views.index'),
    (r'keyserver/user/auth$', 'keyserver.views.auth'),
    (r'keyserver/user/logout$', 'keyserver.views.logout_session'),
    (r'keyserver/user/activate$' , 'keyserver.views.activate'), 
    (r'keyserver/user/profile/get$', 'keyserver.views.getuserprofile'),
    (r'keyserver/user/activated$', 'keyserver.views.activated'),
    (r'keyserver/pubkey/get$', 'keyserver.views.getpubkey'),
    (r'keyserver/message/get$', 'keyserver.views.getmessage'),
    (r'keyserver/msgkey/get$', 'keyserver.views.getmsgkey'),
    (r'keyserver/message/send$', 'keyserver.views.sendmessage'),
    (r'keyserver/contacts/get$',  'keyserver.views.getcontacts'),
    (r'keyserver/msgkey/send$',  'keyserver.views.sendmsgkey'),
    (r'^$', 'web.views.index'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/auth/request$', 'web.views.authrequest'),
    url(r'^accounts/profile/$', 'web.views.profile'),
    url(r'^accounts/logout/$', 'web.views.logout_view'),
        
    # Examples
    # url(r'^$', 'secdef.views.home', name='home'),
    # url(r'^secdef/', include('secdef.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
