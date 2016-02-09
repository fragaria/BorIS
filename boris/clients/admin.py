# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils.dateformat import format
from django.utils.formats import get_format
from django.utils.html import escape, escapejs

from boris.clients.models import Client, Town, Anamnesis, DrugUsage, \
    RiskyManners, Region, District, DiseaseTest, Anonymous, \
    PractitionerContact, Person, GroupContact, ClientCard
from boris.clients.forms import ReadOnlyWidget
from boris.clients.utils import ReadOnlyAdmin
from boris.clients.views import add_note, delete_note
from boris.services.admin import EncounterInline
from boris.utils.admin import BorisBaseAdmin, textual
from boris.utils.widgets import SplitDateWidget


class DrugUsageInline(admin.StackedInline):
    model = DrugUsage
    extra = 0
    fieldsets = (
        (None, {'fields': (
            ('drug', 'application', 'is_primary'),
            ('frequency',),
            ('first_try_age', 'first_try_iv_age', 'first_try_application'),
            ('was_first_illegal',),
            ('note')
        )}),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class RiskyMannersInline(admin.TabularInline):
    model = RiskyManners
    extra = 0


class DiseaseTestInline(admin.TabularInline):
    model = DiseaseTest
    extra = 0


class EnumAdmin(BorisBaseAdmin):
    def show_save(self, obj):
        return True

    def show_save_and_continue(self, obj):
        return False


class AnamnesisAdmin(BorisBaseAdmin):
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
    raw_id_fields = ('filled_where', 'client')
    autocomplete_lookup_fields = {
        'fk': ['filled_where', 'client']
    }

    inlines = (DiseaseTestInline, DrugUsageInline, RiskyMannersInline)

    def client_link(self, obj):
        return u'<a href="%s" style="font-weight: bold">%s</a>' % (
            obj.client.get_admin_url(), obj.client)
    client_link.allow_tags = True
    client_link.short_description = _(u'Klient')

    def client__sex(self, obj):
        if obj.pk:
            return obj.client.get_sex_display()
        return _(u'(Dostupné po uložení anamnézy)')
    client__sex.short_description = _(u'Pohlaví')

    def client__birthyear(self, obj):
        if obj.pk and obj.client.birthdate:
            return obj.client.birthdate.strftime('%Y')
        elif obj.pk:
            return _(u'(Zatím neznámý)')
        else:
            return _(u'(Dostupné po uložení anamnézy)')
    client__birthyear.short_description = _(u'Rok narození')

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        When popup and client_id in GET, use special widget that doesn't need
        to be filled up.
        """
        request = kwargs.get('request', None)
        if request is not None:
            if request.GET.get('_popup', False) and request.GET.get('client_id') and db_field.name == 'client':
                cid = request.GET.get('client_id')
                kwargs['widget'] = ReadOnlyWidget(cid, Client.objects.get(pk=cid))
                kwargs['initial'] = cid
                kwargs.pop('request')
                return db_field.formfield(**kwargs)
            if db_field.name == 'author':
                kwargs['initial'] = request.user.pk
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
        if "_popup" in request.REQUEST and not '_continue' in request.REQUEST.dicts[0]:
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return super(AnamnesisAdmin, self).response_change(request, obj)

    def show_save(self, obj):
        return True

    def force_show_delete(self, obj):
        return obj and obj.pk is not None


class PersonAdmin(BorisBaseAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class AddContactAdmin(BorisBaseAdmin):
    list_actions = ('change_button', 'add_contact_button')

    def queryset(self, request):
        return super(AddContactAdmin, self).queryset(request).extra(
            select={
                'ecnt': 'SELECT COUNT(*) FROM services_encounter '
                        'WHERE services_encounter.person_id = clients_person.id'
            }
        )

    def encounter_count(self, obj):
        return obj.ecnt
    encounter_count.short_description = _(u'Počet kontaktů')
    encounter_count.admin_order_field = 'ecnt'

    def add_contact_button(self, obj):
        return u'<a href="%s" class="changelink cbutton high1">%s</a>' % (
            reverse('admin:services_encounter_add') + '?person_id=%s' % obj.pk,
            _(u'přidat kontakt'))


class AnonymousAdmin(AddContactAdmin):
    change_form_template = 'admin/clients/person/change_form.html'
    inlines = (EncounterInline,)
    readonly_fields = ('drug_user_type', 'sex')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PractitionerContactAdmin(BorisBaseAdmin):
    list_display = ('date', 'town', 'person_or_institution', 'note', 'user_list')
    list_filter = ('date', 'town', 'users')
    date_hierarchy = 'date'
    search_fields = ('person_or_institution', 'note')
    raw_id_fields = ('town',)
    autocomplete_lookup_fields = {
        'fk': ['town', ]
    }
    ordering = ('-date', 'person_or_institution')
    fields = ('person_or_institution', 'town', 'date', 'note', 'users')

    @textual(_(u'Kdo'))
    def user_list(self, obj):
        return u'<br />'.join([unicode(s) for s in obj.users.all()])

    def show_save_and_add_another(self, obj):
        return bool(obj.pk)


# this class assumes being readonly. should this change, the GroupContact's postsave signal needs to be taken care of
class GroupContactAdmin(ReadOnlyAdmin):
    list_display = ('date', 'town', 'name', 'note', 'user_list', 'client_count')
    list_filter = ('date', 'town', 'users')
    date_hierarchy = 'date'
    search_fields = ('name', 'note')
    raw_id_fields = ('town',)
    autocomplete_lookup_fields = {
        'fk': ['town', ]
    }
    ordering = ('-date', 'name')
    fields = ('name', 'town', 'date', 'note', 'users', 'clients')
    filter_horizontal = ('clients', )

    @textual(_(u'Kdo'))
    def user_list(self, obj):
        return u'<br />'.join([unicode(s) for s in obj.users.all()])

    @textual(_(u'Počet klientů'))
    def client_count(self, obj):
        return obj.clients.count()


class ClientCardInline(admin.StackedInline):
    model = ClientCard
    classes = ('grp-collapse', 'grp-closed',)
    template = 'admin/services/encounter/client_card_inline.html'
    extra = 0


class ClientAdmin(AddContactAdmin):
    list_display = ('code', 'first_name_display', 'last_name_display', 'sex',
                    'town', 'encounter_count')
    list_filter = ('town', 'sex', 'primary_drug', 'encounters__performed_on')
    search_fields = ('code', 'first_name', 'last_name')
    fieldsets = (
        (_(u'Základní informace'), {'fields': (
            ('code', 'sex'),
            ('town',),
            ('first_name', 'last_name'),
            ('birthdate', 'birthdate_year_only'),
            ('close_person', 'sex_partner'),
            ('primary_drug', 'primary_drug_usage'),
            ('first_contact_verbose', 'last_contact_verbose'),
            'anamnesis_link',
        )}),
    )
    raw_id_fields = ('town',)
    autocomplete_lookup_fields = {
        'fk': ['town', ]
    }
    readonly_fields = (u'anamnesis_link', 'first_contact_verbose', 'last_contact_verbose')
    inlines = (ClientCardInline, EncounterInline,)

    @textual(_(u'Jméno'), 'first_name')
    def first_name_display(self, obj):
        return obj.first_name

    @textual(_(u'Příjmení'), 'first_name')
    def last_name_display(self, obj):
        return obj.last_name

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {
            'current_date': datetime.now().strftime('%d.%m.%Y'),
            'current_time': datetime.now().strftime('%H:%M'),
        }
        return super(ClientAdmin, self).change_view(request, object_id,
            extra_context=extra_context)

    formfield_overrides = {
        models.DateField: {'widget': SplitDateWidget},
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
            return u'<a class="cbutton" href="%s?client_id=%s" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                obj.anamnesis.get_admin_url(), obj.pk, _(u'Zobrazit'))
        else:
            return '<a class="cbutton" href="%s?client_id=%s" id="add_id_anamnesis" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                reverse('admin:clients_anamnesis_add'), obj.pk, _(u'Přidat anamnézu'))
    anamnesis_link.allow_tags = True
    anamnesis_link.short_description = _(u'Anamnéza')

    def button_captions(self, obj):
        if obj.pk:
            # Avoid misunderstandings when deleting inline encounters.
            return {
                'BO_SAVE_CAPTION': _(u'Uložit změny'),
                'BO_DELETE_CAPTION': _(u'Odstranit klienta')
            }
        return {}


admin.site.register(Region, EnumAdmin)
admin.site.register(District, EnumAdmin)
admin.site.register(Town, EnumAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PractitionerContact, PractitionerContactAdmin)
admin.site.register(GroupContact, GroupContactAdmin)
admin.site.register(Anonymous, AnonymousAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Anamnesis, AnamnesisAdmin)

