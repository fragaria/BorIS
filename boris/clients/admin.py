# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from boris.clients.models import Client, Drug, ClientNote, Town,\
    RiskyBehavior, Anamnesis, DrugUsage, RiskyManners


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
        return '<a href="/clients/client/%i" style="font-weight: bold">%s</a>' % (obj.client.pk, obj.client)
    client_link.allow_tags = True
    client_link.short_description = u'Klient'


class ClientModelAdmin(admin.ModelAdmin):
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

    def anamnesis_link(self, obj):
        try:
            if obj.pk:
                anamnesis = obj.anamnesis
            else:
                anamnesis = -1
        except Anamnesis.DoesNotExist:
            anamnesis = None

        if anamnesis == -1:
            return u'(Nejdřív prosím uložte klienta)'
        elif anamnesis:
            return '<a href="/clients/anamnesis/%i">Anamnéza</a>' % obj.anamnesis.pk
        else:
            return '<a href="/clients/anamnesis/add" id="add_id_anamnesis" onclick="return showAddAnotherPopup(this);">Přidat anamnézu</a>'
    anamnesis_link.allow_tags = True
    anamnesis_link.short_description = u'Anamnéza'


admin.site.register(RiskyBehavior)
admin.site.register(Drug)
admin.site.register(Town)
admin.site.register(Client, ClientModelAdmin)
admin.site.register(ClientNote)
admin.site.register(Anamnesis, AnamnesisAdmin)

