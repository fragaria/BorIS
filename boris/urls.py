from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from boris.reporting.admin import interface

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Django grappelli
    (r'^grappelli/', include('grappelli.urls')),

    (r'^reporting/', include(interface.urls)),
    (r'^services/', include('boris.services.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

