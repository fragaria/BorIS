# -*- coding: utf-8 -*-
from django.contrib import admin

from boris.clients.models import Client, Drug, ClientNote, Town, RiskyBehavior, Anamnesis


class AnamnesisInline(admin.StackedInline):
    # TODO: this doesn't look well - perhaps should be displayed separately
    model = Anamnesis

    fieldsets = (
        (u'Metainformace', {'fields': (
            ('filled_when', 'filled_where', 'district', 'region', 'author' ),)}),
        (u'Základní informace', {'fields': (
            ('nationality', 'ethnic_origin'),
            ('living_condition', 'accomodation', 'lives_with_junkies'),
            ('employment', 'education'),
            ('hiv_examination', 'hepatitis_examination', 'been_cured_before', 'been_cured_currently'),
            )}),
    )

class ClientModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (u'Základní informace', {'fields': (
            ('code', 'sex', 'town'),
            ('first_name', 'last_name'),
            'birthdate',
            ('primary_drug', 'primary_drug_usage'),
            )}),
    )

    inlines = (AnamnesisInline, )

admin.site.register(RiskyBehavior)
admin.site.register(Drug)
admin.site.register(Town)
admin.site.register(Client, ClientModelAdmin)
admin.site.register(ClientNote)
admin.site.register(Anamnesis)
