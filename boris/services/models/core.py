# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from datetime import date

from django.db import models
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager

from boris.services.forms import ServiceForm
from boris.utils.forms import adminform_formfield

class Encounter(models.Model):
    client = models.ForeignKey('clients.Client', related_name='encounters',
        verbose_name=_(u'Klient'))
    performed_by = models.ManyToManyField('auth.User', verbose_name=_(u'Kdo'))
    performed_on = models.DateField(default=date.today, verbose_name=_(u'Kdy'))
    where = models.ForeignKey('clients.Town', verbose_name=_(u'Kde'))
    
    class Meta:
        app_label = 'services'
        verbose_name = _(u'Kontakt')
        verbose_name_plural = _(u'Kontakty')
        ordering = ('-performed_on',)
        
    def __unicode__(self):
        return unicode(self.client)


class ServiceOptions(object):
    def __init__(self):
        self.title = ''
        self.description_template = None
        self.available = lambda client: False
        
    def is_available(self, client):
        return self.available(client)
    
    def get_title(self):
        return self.title
    
    def get_description_template_list(self):
        return (self.description_template, 'services/desc/default.html')
    
    def get_description(self):
        from django import template
        t = template.loader.select_template(self.get_description_template_list())
        return t.render(template.Context())
        

class ClientServiceMetaclass(models.Model.__metaclass__):
    registered_services = []
    
    def __new__(cls, name, bases, attrs):
        new_cls = super(ClientServiceMetaclass, cls).__new__(cls, name, bases, attrs)
        
        if not new_cls._meta.abstract:
            cls.registered_services.append(new_cls)
            
        service_meta = {
            'title': new_cls._meta.verbose_name,
            'description_template': 'services/desc/%s.html' % name.lower(),
            'available': lambda client: not new_cls._meta.abstract,
        }
        attrs_service_meta = attrs.pop('Service', None)
        
        if attrs_service_meta:
            service_meta.update(attrs_service_meta.__dict__)
            
        new_cls.service = ServiceOptions()
        new_cls.service.__dict__.update(service_meta)
        
        return new_cls
    
    
class ClientService(TimeStampedModel):
    __metaclass__ = ClientServiceMetaclass
    
    encounter = models.ForeignKey(Encounter, related_name='services',
        verbose_name=_(u'Kontakt'))
    title = models.CharField(max_length=255, editable=False,
        verbose_name=_(u'Název'))
    
    objects = InheritanceManager()
    
    class Meta:
        app_label = 'services'
        ordering = ('encounter',)


    class Service:
        available = lambda client: False
        

    def __unicode__(self):
        return self.title
    
    def _prepare_title(self):
        return self.service.get_title()
    
    def clean(self):
        super(ClientService, self).clean()
        self.title = force_unicode(self._prepare_title())
        
    @classmethod
    def form(cls):
        from django.forms.models import modelform_factory
        return modelform_factory(cls, form=ServiceForm,
            formfield_callback=adminform_formfield)
    
    @classmethod
    def class_name(cls):
        return cls.__name__
    
    
def service_list(client, available_only=True):
    """
    Returns tuple of client services registered in application.
    
    When `available_only` parameter is used, only those that can be provided
    to `client` will be listed.
    """
    if available_only:
        return (s for s in ClientService.registered_services if s.service.is_available(client))
    return ClientService.registered_services


def get_model_for_class_name(class_name):
    """Returns ClientService model class for given name"""
    for s in ClientService.registered_services:
        if s.__name__ == class_name:
            return s
    raise ValueError('Service `%s` is not registered' % class_name)
