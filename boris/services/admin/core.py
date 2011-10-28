# -*- coding: utf-8 -*-
'''
Created on 27.10.2011

@author: xaralis
'''
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from boris.services.models.core import Encounter
from boris.clients.forms import ReadOnlyWidget
from django import forms

class EncounterAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('client', 'performed_on', 'where'), 'performed_by')}),
    )
    raw_id_fields = ('where',)
    autocomplete_lookup_fields = {
        'fk': ['where',]
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        When popup and client_id in GET, use special widget that doesn't need
        to be filled up.
        """
        from boris.clients.models import Client
        
        request = kwargs.get('request', None)
        if request is not None and request.GET.get('client_id') and db_field.name == 'client':
            cid = request.GET.get('client_id')
            kwargs.pop('request')
            kwargs['widget'] = ReadOnlyWidget(cid, Client.objects.get(pk=cid))
            kwargs['initial'] = cid
            return db_field.formfield(**kwargs)
        elif db_field.name == 'performed_by':
            kwargs.pop('request')
            kwargs['widget'] = forms.SelectMultiple(attrs={'style': 'height: 70px;'})
            return db_field.formfield(**kwargs)
        else:
            return super(EncounterAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Encounter, EncounterAdmin)