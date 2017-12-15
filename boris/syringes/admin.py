# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms

from boris.syringes.models import SyringeCollection
from boris.utils.admin import BorisBaseAdmin, textual


class SyringeCollectionForm(forms.ModelForm):
    class Meta:
        model = SyringeCollection

    def __init__(self, *args, **kwargs):
        super(SyringeCollectionForm, self).__init__(*args, **kwargs)
        self.fields['persons'].queryset = self.fields['persons'].queryset.filter(is_active=True)


class SyringeCollectionAdmin(BorisBaseAdmin):
    form = SyringeCollectionForm
    raw_id_fields = ('town',)
    autocomplete_lookup_fields = {
        'fk': ('town',),
    }
    list_display = ('date', 'town', 'location_display', 'count', 'user_list')
    list_filter = ('date', 'town', 'persons')
    date_hierarchy = 'date'
    fields = ('count', 'town', 'date', 'location', 'persons')
    ordering = ('-date',)

    @textual(_(u'Kdo'))
    def user_list(self, obj):
        return u'<br />'.join([unicode(s) for s in obj.persons.all()])

    @textual(_(u'Kde (např. u silnice)'), 'location')
    def location_display(self, obj):
        return unicode(obj.location)

    def show_save_and_add_another(self, obj): return bool(obj.pk)

admin.site.register(SyringeCollection, SyringeCollectionAdmin)
