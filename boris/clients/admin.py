# -*- coding: utf-8 -*-
from anyjson import serialize

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.utils.translation import ugettext as _
from django.utils.dateformat import format
from django.utils.formats import get_format

from boris.clients.models import Client, Drug, ClientNote, Town,\
    RiskyBehavior, Anamnesis, DrugUsage, RiskyManners
from django.core.urlresolvers import reverse


class DrugUsageInline(admin.StackedInline):
    model = DrugUsage
    extra = 0
    fields = (
            ('drug', 'application', 'is_primary'),
            ('frequency', ),
            ('first_try_age', 'first_try_iv_age', 'first_try_application'),
            ('was_first_illegal', ),
            ('note'),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class RiskyMannersInline(admin.TabularInline):
    model = RiskyManners
    extra = 0


class AnamnesisAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'client_link')
    search_fields = ('client__code', 'client__first_name', 'client__last_name')
    fields = (
            ('client', ),
            ('filled_when', 'filled_where', 'author'),
            ('nationality', 'ethnic_origin'),
            ('living_condition', 'accomodation'),
            'lives_with_junkies',
            ('employment', 'education'),
            ('hiv_examination', 'hepatitis_examination'),
            ('been_cured_before', 'been_cured_currently'),
            ('district', 'region')
    )

    inlines = (DrugUsageInline, RiskyMannersInline)


    def client_link(self, obj):
        return '<a href="%s" style="font-weight: bold">%s</a>' % (
            obj.client.get_admin_url(), obj.client)
    client_link.allow_tags = True
    client_link.short_description = _(u'Klient')


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('code', 'first_name', 'last_name')
    fieldsets = (
        (u'Základní informace', {'fields': (
            ('code', 'sex', 'town'),
            ('first_name', 'last_name'),
            'birthdate',
            ('primary_drug', 'primary_drug_usage'),
            'anamnesis_link',
            )}),
    )

    readonly_fields = (u'anamnesis_link', )
    
    def get_urls(self):
        urls = super(ClientAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<object_id>\d+)/add-note/$',
                self.admin_site.admin_view(self.add_note),
                name='clients_add_note'
            ),
        )
        return my_urls + urls

    def anamnesis_link(self, obj):
        try:
            if obj.pk:
                anamnesis = obj.anamnesis
            else:
                anamnesis = -1
        except Anamnesis.DoesNotExist:
            anamnesis = None

        if anamnesis == -1:
            return _(u'(Nejdřív prosím uložte klienta)')
        elif anamnesis:
            return u'<a href="%s">%s</a>' % (
                obj.anamnesis.get_admin_url(), _(u'Zobrazit &raquo;'))
        else:
            return '<a href="%s" id="add_id_anamnesis" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                reverse('admin:clients_anamnesis_add'), _(u'Přidat anamnézu'))
    anamnesis_link.allow_tags = True
    anamnesis_link.short_description = _(u'Anamnéza')
    
    def add_note(self, request, object_id):
        if not request.method == 'POST' or not request.POST.get('text') or not request.is_ajax():
            raise Http404

        try:
            client = Client.objects.get(pk=object_id)
        except (Client.DoesNotExist, ValueError):
            return HttpResponseBadRequest()

        client_note = ClientNote.objects.create(author=request.user,
            text=request.POST['text'], client=client)

        ret = {
            'author': client_note.author.username,
            'datetime': format(client_note.datetime, get_format('DATE_FORMAT')),
            'text': client_note.text,
        }

        return HttpResponse(serialize(ret))
    
admin.site.register(RiskyBehavior)
admin.site.register(Drug)
admin.site.register(Town)
admin.site.register(Client, ClientAdmin)
admin.site.register(Anamnesis, AnamnesisAdmin)

