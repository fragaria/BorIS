from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from boris.clients.views import add_client_note

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^clients/add-note/', add_client_note, name='add-client-note'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

