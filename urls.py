from django.conf.urls.defaults import *
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
#    url(r'^admin$', include(admin.site.urls)),
    url(r'^', include('portal.urls')),
    )


