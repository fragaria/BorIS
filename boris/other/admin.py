# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from boris.other.models import SyringeCollection

def user_list(self, obj):
    return u'<br />'.join([unicode(s) for s in obj.persons.all()])
user_list.short_description = _(u'Kdo')
user_list.allow_tags = True

class SyringeCollectionAdmin(admin.ModelAdmin):

    raw_id_fields = ('town','persons',)
    autocomplete_lookup_fields = {
        'fk': ['town',],
        'm2m': ['persons',],
    }
    list_display = ('date', 'town', 'location', 'count', 'user_list')
    list_filter = ('date', 'town',)

    class Meta:
        model = SyringeCollection

SyringeCollectionAdmin.user_list = user_list


admin.site.register(SyringeCollection, SyringeCollectionAdmin)
