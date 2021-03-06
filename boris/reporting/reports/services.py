# -*- coding: utf-8 -*-
from django.template import loader
from django.template.context import RequestContext

from boris.clients.models import Client
from boris.reporting.core import BaseReport
from boris.services.models import service_list, Encounter, TimeDotation


class ServiceReport(BaseReport):
    title = u'Shrnutí výkonů'
    description = u'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype_office = 'application/vnd.ms-word; charset=utf-8'

    def __init__(self, date_from=None, date_to=None, towns=None, person=None, towns_residence=None):
        clients = Client.objects.all()
        if towns_residence is not None:
            clients = clients.filter(town__in=towns_residence)
        client_ids = clients.values_list('id', flat=True)

        enc_filtering = (
            ('performed_on__gte', date_from),
            ('performed_on__lte', date_to),
            ('where__in', towns),
            ('person__id__in', client_ids),
            ('person', person),
        )
        enc_filtering = [(f[0], f[1]) for f in enc_filtering if f[1]]
        filtering = [('encounter__%s' % f[0], f[1]) for f in enc_filtering]

        self.enc_filtering = dict(enc_filtering)
        self.filtering = dict(filtering)
        self.date_from = date_from
        self.date_to = date_to
        self.towns = towns
        self.towns_residence = towns_residence
        self.person = person

    def get_filename(self):
        return 'souhrn_vykonu.doc'

    def _get_service_stats(self):
        services = self._get_services()
        return [service.get_stats(self.filtering) for service in services]

    def _get_services(self):
        services = [service for service in service_list(self.person, diseases_last=True)
                    if service.service.include_in_reports]
        return services

    def _get_service_time(self):
        services = self._get_services()
        filtering = self.filtering

        total_time_spent = 0
        for service in services:
            enc_ids = service.objects.filter(**filtering).values_list('encounter__id', flat=True)
            total_time_spent += TimeDotation.time_spent_on_encounters(enc_ids, service)
        time_stats = (u'Celkový čas poskytnutých výkonů (hod)', '%.2f' % (float(total_time_spent)/60.0))
        return [(TimeDotation, (time_stats,))]

    def get_stats(self):
        encounters = Encounter.objects.filter(**self.enc_filtering)
        all_enc_count = encounters.count()
        direct_enc_count = encounters.filter(is_by_phone=False).count()
        encounter_stats = (u'Počet kontaktů (z toho přímých)', '%i (%i)' % (
            all_enc_count, direct_enc_count))
        return [(None, (encounter_stats,))] + self._get_service_stats() + self._get_service_time()

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'stats': self.get_stats(),
                'person': self.person,
                'date_from': self.filtering.get('encounter__performed_on__gte'),
                'date_to': self.filtering.get('encounter__performed_on__lte'),
                'towns': self.towns,
                'towns_residence': self.towns_residence,
            },
            context_instance=RequestContext(request)
        )
