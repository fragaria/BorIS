# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _

from boris.classification import DRUG_APPLICATION_TYPES as DAT
from boris.clients.models import Client
from boris.reporting.core import BaseReport
from boris.services.models import Encounter


def enrich_with_type(client):
    """Enrich client with his/her 'type', as understood by this report."""
    if client.close_person:
        client.type_ = _(u'Osoba blízká')
    elif client.sex_partner:
        client.type_ = _(u'Sexuální partner')
    elif client.primary_drug_usage in (DAT.VEIN_INJECTION, DAT.MUSCLE_INJECTION):
        client.type_ = _(u'IV uživatel')
    else:
        client.type_ = _(u'neIV uživatel')


class ClientReport(BaseReport):
    title = u'Shrnutí klientů'
    description = (u'Přehled klientů splňujících zadaná kritéria. '
        u'Město ve formuláři označuje místo, kde byl zaznamenán kontakt s klientem.')
    contenttype_office = 'application/vnd.ms-excel; charset=utf-8'
    columns = (_(u'Klientský kód'), _(u'Pohlaví'), _(u'Město'),
        _(u'Typ klienta'), _(u'Primární droga'))

    def __init__(self, date_from=None, date_to=None, towns=None):
        client_contenttype = ContentType.objects.get_by_natural_key('clients',
            'Client')
        filtering = (
            ('performed_on__gte', date_from),
            ('performed_on__lte', date_to),
            ('where__in', towns),
            ('person__content_type', client_contenttype),
        )
        filtering = ((f[0], f[1]) for f in filtering if f[1])
        self.filtering = dict(filtering)
        self.date_from = date_from
        self.date_to = date_to
        self.towns = towns

    def get_filename(self):
        return 'souhrn_klientu.xls'

    def get_stats(self):
        person_ids = Encounter.objects.filter(**self.filtering).values_list(
            'person', flat=True) # distinct() cannot be used here because
                                 # Encounters are ordered by default.
        clients = Client.objects.filter(person_ptr__in=person_ids).order_by(
            'code')
        for client in clients:
            enrich_with_type(client)
        return clients

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'report': self,
                'stats': self.get_stats(),
                'towns': [t.title for t in self.towns],
                'date_from': self.date_from,
                'date_to': self.date_to
            },
            context_instance=RequestContext(request)
        )
