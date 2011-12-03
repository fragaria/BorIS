'''
Created on 3.12.2011

@author: xaralis
'''
from django.contrib.admin.sites import AdminSite

class BorisAdminSite(AdminSite):
    def get_urls(self):
        from boris.reporting.views import interface
        return super(BorisAdminSite, self).get_urls() + interface.get_urls()
    
    
site = BorisAdminSite()