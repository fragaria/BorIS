'''
Created on 27.11.2011

@author: xaralis
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('boris.reporting.views',
    url('^monthly-stats/$', 'monthly_stats'),
)