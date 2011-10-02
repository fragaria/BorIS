# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .core import ClientService

class AsistService(ClientService):
    where = models.CharField(max_length=255, verbose_name=_(u'Kam'))
    note = models.TextField(null=True, blank=True, verbose_name=_(u'Poznámka'))
    
    class Meta:
        app_label = 'services'
        verbose_name = _(u'Asistenční služba')
        verbose_name_plural = _(u'Asistenční služby')
        
    def _prepare_title(self):
        return _(u'%(title)s: doprovod %(where)s') % {
            'title': self.service['title'], 'where': self.where
        }
        
