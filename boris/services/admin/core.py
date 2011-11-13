# -*- coding: utf-8 -*-
'''
Created on 27.10.2011

@author: xaralis
'''
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from boris.services.models.core import Encounter
from boris.clients.forms import ReadOnlyWidget


class EncounterInline(admin.TabularInline):
    model = Encounter
    fieldsets = (
        (None, {'fields': ('performed_on', 'where', 'performed_by_verbose', 'service_count', 'service_list', 'goto_link')}),
    )
    readonly_fields = ('performed_by_verbose', 'service_count', 'service_list',
        'goto_link')
    extra = 0
    max_num = 0
    
    def performed_by_verbose(self, obj):
        return u', '.join([unicode(u) for u in obj.performed_by.all()])
    performed_by_verbose.short_description = _(u'Provedli')

    def service_list(self, obj):
        return u'<small>' + u'<br />'.join([unicode(s) for s in obj.services.all()]) + u'</small>'
    service_list.short_description = _(u'Provedené výkony')
    service_list.allow_tags = True

    def goto_link(self, obj):
        if obj.pk:
            return u'<a href="%s"><strong>%s &raquo;</strong></a>' % (obj.get_admin_url(), _(u'Přejít'))
        else:
            return _(u'Detaily kontaktu je možné editovat až po uložení.')
    goto_link.short_description = _(u'Přejít')
    goto_link.allow_tags = True


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

    def response_change(self, request, obj):
        if '_continue' not in request.POST and '_addanother' not in request.POST:
            dest = reverse('admin:clients_client_change', args=[obj.client.pk])
            return HttpResponseRedirect(dest)
        else:
            return super(EncounterAdmin, self).response_change(request, obj)


admin.site.register(Encounter, EncounterAdmin)

