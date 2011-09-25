# -*- coding: utf-8 -*-
from django.contrib import admin

from boris.clients.models import Client, Drug, ClientNote, Town, DrugUsage,\
    RiskyManners, RiskyBehavior

class DrugUsageInline(admin.TabularInline):
    model = DrugUsage
    

class RiskyMannersInline(admin.TabularInline):
    model = RiskyManners    


class ClientModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (u'Základní informace', {'fields': (
            ('code', 'sex', 'town'), ('first_name', 'last_name'), 'birthdate')}),
        (u'Vstupní dotazník', {'fields': (
            ('nationality', 'ethnic_origin'), ('living_condition', 'accomodation'),
            'lives_with_junks', ('employment', 'education'),
            ('hiv_examination', 'hepatitis_examination'),
            ('been_cured_before', 'been_cured_currently'), ('district', 'region'))})
    )
    inlines = (DrugUsageInline, RiskyMannersInline)


admin.site.register(RiskyBehavior)
admin.site.register(Drug)
admin.site.register(Town)
admin.site.register(Client, ClientModelAdmin)
admin.site.register(ClientNote)

