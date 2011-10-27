# -*- coding: utf-8 -*-
from datetime import datetime, date

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
from django.forms.extras.widgets import SelectDateWidget

from django.http import HttpResponse

from django.utils.translation import ugettext as _
from django.utils.dateformat import format
from django.utils.formats import get_format
from django.utils.html import escape, escapejs

from boris.clients.models import Client, Drug, Town, RiskyBehavior, Anamnesis,\
     DrugUsage, RiskyManners, Region, District, DiseaseTest
from boris.clients.forms import ReadOnlyWidget
from boris.clients.views import add_note, delete_note

class DrugUsageInline(admin.StackedInline):
    model = DrugUsage
    extra = 0
    fieldsets = (
        (None, {'fields': (
            ('drug', 'application', 'is_primary'),
            ('frequency', ),
            ('first_try_age', 'first_try_iv_age', 'first_try_application'),
            ('was_first_illegal', ),
            ('note')
        )}),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class RiskyMannersInline(admin.TabularInline):
    model = RiskyManners
    extra = 0

class DiseaseTestInline(admin.TabularInline):
    model = DiseaseTest
    extra = 0


class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'client_link')
    search_fields = ('client__code', 'client__first_name', 'client__last_name')
    readonly_fields = ('client__sex', 'client__birthyear')
    fieldsets = (
        (
            _(u'Základní klientská data'),
            {
                'description': _(u'Případné změny v této sekci prosím provádějte přímo na kartě klienta'),
                'fields': (('client', 'client__sex', 'client__birthyear'),),
            }
        ),
        (
            _(u'Kontakt'),
            {
                'fields': (
                    ('author', 'filled_when',),
                    ('filled_where',),
                ),
            }
        ),
        (_(u'Anamnestické údaje'), {'fields': (
            ('nationality', 'ethnic_origin'),
            ('living_condition', 'accomodation'),
            'lives_with_junkies',
            ('employment', 'education'),
            ('been_cured_before', 'been_cured_currently'),
        )}),
    )
    raw_id_fields = ('filled_where',)
    autocomplete_lookup_fields = {
        'fk': ['filled_where',]
    }

    inlines = (DiseaseTestInline, DrugUsageInline, RiskyMannersInline)

    def client_link(self, obj):
        return '<a href="%s" style="font-weight: bold">%s</a>' % (
            obj.client.get_admin_url(), obj.client)
    client_link.allow_tags = True
    client_link.short_description = _(u'Klient')

    def client__sex(self, obj):
        return obj.client.get_sex_display()
    client__sex.short_description = _(u'Pohlaví')

    def client__birthyear(self, obj):
        if obj.client.birthdate:
            return obj.client.birthdate.strftime('%Y')
        else:
            return _(u'(Zatím neznámý)')
    client__birthyear.short_description = _(u'Rok narození')

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        When popup and client_id in GET, use special widget that doesn't need
        to be filled up.
        """
        request = kwargs.get('request', None)
        if request is not None and request.GET.get('_popup', False) and request.GET.get('client_id') and db_field.name == 'client':
            cid = request.GET.get('client_id')
            kwargs.pop('request')
            kwargs['widget'] = ReadOnlyWidget(cid, Client.objects.get(pk=cid))
            kwargs['initial'] = cid
            return db_field.formfield(**kwargs)
        else:
            return super(AnamnesisAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Overriden to use special callback when closing popup.
        """

        if "_popup" in request.POST and "_continue" not in request.POST:
            # @attention: Change function call
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnamnesisPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(obj._get_pk_val()), escapejs(obj)))
        else:
            return super(AnamnesisAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_popup" in request.REQUEST:
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return super(AnamnesisAdmin, self).response_change(request, obj)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('code', 'first_name', 'last_name', 'sex', 'town')
    list_filter = ('town', 'sex', 'primary_drug')
    search_fields = ('code', 'first_name', 'last_name')
    fieldsets = (
        (_(u'Základní informace'), {'fields': (
            ('code', 'sex', 'town'),
            ('first_name', 'last_name'),
            ('birthdate', 'birthdate_year_only'),
            ('primary_drug', 'primary_drug_usage'),
            ('first_contact_verbose', 'last_contact_verbose'),
            'anamnesis_link',
            )}),
    )
    raw_id_fields = ('town',)
    autocomplete_lookup_fields = {
        'fk': ['town',]
    }
    readonly_fields = (u'anamnesis_link', 'first_contact_verbose', 'last_contact_verbose')

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {
            'current_date': datetime.now().strftime('%d.%m.%Y'),
            'current_time': datetime.now().strftime('%H:%M'),
        }
        return super(ClientAdmin, self).change_view(request, object_id,
            extra_context=extra_context)


    class SelectBornDateWidget(SelectDateWidget):
        """
        Extend to avoid passing attrs to formfield_overrides - because
        if we did, admin would work only when web servery is just refreshed,
        on second view, it would be wasted :(
        """
        def __init__(self, attrs=None, required=True):
            super(ClientAdmin.SelectBornDateWidget, self).__init__(
                attrs=attrs, required=required,
                years=reversed(range(date.today().year - 100, date.today().year + 1))
            )
    formfield_overrides = {
        models.DateField: {'widget': SelectBornDateWidget},
    }

    def get_urls(self):
        urls = super(ClientAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^add-note/$',
                self.admin_site.admin_view(add_note),
                name='clients_add_note'
            ),
            url(r'^delete-note/(?P<note_id>\d+)/$',
                self.admin_site.admin_view(delete_note),
                name='clients_delete_note'
            ),
        )
        return my_urls + urls

    def _contact_verbose(self, val):
        if val is None:
            return _(u'(Není známo)')
        else:
            return format(val, get_format('DATE_FORMAT'))

    def first_contact_verbose(self, obj):
        return self._contact_verbose(obj.first_contact_date)
    first_contact_verbose.short_description = _(u'Datum prvního kontaktu')

    def last_contact_verbose(self, obj):
        return self._contact_verbose(obj.last_contact_date)
    last_contact_verbose.short_description = _(u'Datum posledního kontaktu')

    def anamnesis_link(self, obj):
        try:
            anamnesis = obj.anamnesis if obj.pk else -1
        except Anamnesis.DoesNotExist:
            anamnesis = None

        if anamnesis == -1:
            return _(u'(Nejdřív prosím uložte klienta)')
        elif anamnesis:
            return u'<a href="%s?client_id=%s" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                obj.anamnesis.get_admin_url(), obj.pk, _(u'Zobrazit &raquo;'))
        else:
            return '<a href="%s?client_id=%s" id="add_id_anamnesis" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                reverse('admin:clients_anamnesis_add'), obj.pk, _(u'Přidat anamnézu'))
    anamnesis_link.allow_tags = True
    anamnesis_link.short_description = _(u'Anamnéza')



admin.site.register(RiskyBehavior)
admin.site.register(Drug)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Town)
admin.site.register(Client, ClientAdmin)
admin.site.register(Anamnesis, AnamnesisAdmin)

