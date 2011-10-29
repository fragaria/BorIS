'''
Created on 2.10.2011

@author: xaralis
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('boris.services.views',
    url(r'handle-form/(?P<encounter_id>\d+)/(?P<service_cls>[a-zA-Z]+)/$', 'handle_form', name='services_handle_form_add'),
    url(r'handle-form/(?P<encounter_id>\d+)/(?P<service_cls>[a-zA-Z]+)/(?P<object_id>\d+)/$', 'handle_form', name='services_handle_form_change'),
#    url(r'list-for-client/(?P<client_id>\d+)/$', 'services_list', name='services_list'),
    url(r'list-for-encounter/(?P<encounter_id>\d+)/$', 'services_list', name='services_list'),
    url(r'drop/(?P<service_id>\d+)/$', 'drop_service', name='services_drop'),
)