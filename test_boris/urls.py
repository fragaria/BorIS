from django.conf.urls import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # serve static files

    url(r'^', include('boris.urls')),
    url(r'^', include(admin.site.urls)),
)

