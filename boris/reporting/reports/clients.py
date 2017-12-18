# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from numpy import median
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
    columns = (_(u'Klientský kód'), _(u'Pohlaví'), _(u'Věk'), _(u'Město'),
        _(u'Typ klienta'), _(u'Primární droga'))

    def __init__(self, date_from=None, date_to=None, towns=None, services=None, age_to=None, age_from=None):
        client_contenttype = ContentType.objects.get_by_natural_key('clients', 'Client')
        clients = Client.objects.filter_by_age(age_from, age_to)
        client_ids = clients.values_list('id', flat=True)

        filtering = (
            ('performed_on__gte', date_from),
            ('performed_on__lte', date_to),
            ('where__in', towns),
            ('services__content_type__id__in', services),
            ('person__content_type', client_contenttype),
            ('person_id__in', client_ids),
        )
        filtering = ((f[0], f[1]) for f in filtering if f[1] or
                     (f[0] == 'person_id__in' and (age_to is not None or age_from is not None)))
        self.filtering = dict(filtering)
        self.date_from = date_from
        self.date_to = date_to
        self.towns = towns
        self.services = services

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

    @staticmethod
    def get_median_age(client_stats, date_to):
        relative_to = date_to or datetime.date.today()
        ages = filter(bool, (c.get_relative_age(relative_to) for c in client_stats))

        if any(ages):
            median_age = median(ages)
            return int(median_age)

    @staticmethod
    def get_average_age(client_stats, date_to):
        """Return average age of the filtered clients."""
        relative_to = date_to or datetime.date.today()
        ages = filter(bool, (c.get_relative_age(relative_to) for c in client_stats))
        if ages:
            return int(round(float(sum(ages)) / len(ages)))

    def render(self, request, display_type):
        client_stats = self.get_stats()

        return loader.render_to_string(
            self.get_template(display_type),
            {
                'report': self,
                'stats': client_stats,
                'towns': [t.title for t in self.towns],
                'services': self.services,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'average_age': self.get_average_age(client_stats, self.date_to),
                'median_age': self.get_median_age(client_stats, self.date_to)
            },
            context_instance=RequestContext(request)
        )
