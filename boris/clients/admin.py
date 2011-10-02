# -*- coding: utf-8 -*-
from datetime import date
from anyjson import serialize

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
from django.forms.extras.widgets import SelectDateWidget

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext as _
from django.utils.dateformat import format
from django.utils.formats import get_format
from django.utils.encoding import force_unicode
from django.utils.html import escape, escapejs

from boris.clients.models import Client, Drug, ClientNote, Town,\
    RiskyBehavior, Anamnesis, DrugUsage, RiskyManners
from boris.clients.forms import ReadOnlyWidget

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


class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'client_link')
    search_fields = ('client__code', 'client__first_name', 'client__last_name')
    fieldsets = (
        (None, {'fields': (
            'client',
            ('filled_when', 'filled_where', 'author'),
            ('nationality', 'ethnic_origin'),
            ('living_condition', 'accomodation'),
            'lives_with_junkies',
            ('employment', 'education'),
            ('hiv_examination', 'hepatitis_examination'),
            ('been_cured_before', 'been_cured_currently'),
            ('district', 'region'),
        )}),
    )

    inlines = (DrugUsageInline, RiskyMannersInline)

    def client_link(self, obj):
        return '<a href="%s" style="font-weight: bold">%s</a>' % (
            obj.client.get_admin_url(), obj.client)
    client_link.allow_tags = True
    client_link.short_description = _(u'Klient')
    
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
        Determines the HttpResponse for the add_view stage.
        
        Overriden to use special callback when closing popup.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.POST:
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if "_popup" in request.POST:
            # @attention: Change function call
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnamnesisPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = '../'
            else:
                post_url = '../../../'
            return HttpResponseRedirect(post_url)
        

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
            url(r'^(?P<object_id>\d+)/add-note/$',
                self.admin_site.admin_view(self.add_note),
                name='clients_add_note'
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
            return u'<a href="%s" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                obj.anamnesis.get_admin_url(), _(u'Zobrazit &raquo;'))
        else:
            return '<a href="%s?client_id=%s" id="add_id_anamnesis" onclick="return showAddAnotherPopup(this);">%s</a>' % (
                reverse('admin:clients_anamnesis_add'), obj.pk, _(u'Přidat anamnézu'))
    anamnesis_link.allow_tags = True
    anamnesis_link.short_description = _(u'Anamnéza')

    def add_note(self, request, object_id):
        if not request.method == 'POST' or not request.POST.get('text') or not request.is_ajax():
            raise Http404

        client = get_object_or_404(Client, pk=object_id)

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

