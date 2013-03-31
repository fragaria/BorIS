# -*- coding: utf-8 -*-
from django.template import loader
from django.template.context import RequestContext

from boris.reporting.core import BaseReport
from boris.services.models import service_list, Encounter


class ServiceReport(BaseReport):
    title = u'Shrnutí výkonů'
    description = u'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype_office = 'application/vnd.ms-word; charset=utf-8'

    def __init__(self, date_from=None, date_to=None, town=None, person=None):
        enc_filtering = (
            ('performed_on__gte', date_from),
            ('performed_on__lte', date_to),
            ('where', town),
            ('person', person),
        )
        enc_filtering = [(f[0], f[1]) for f in enc_filtering if f[1] is not None]
        filtering = [('encounter__%s' % f[0], f[1]) for f in enc_filtering]

        self.enc_filtering = dict(enc_filtering)
        self.filtering = dict(filtering)
        self.date_from = date_from
        self.date_to = date_to
        self.town = town
        self.person = person

    def get_filename(self):
        return 'souhrn_vykonu.doc'

    def get_stats(self):
        enc_count = Encounter.objects.filter(**self.enc_filtering).count()
        return [(None, ((u'Počet kontaktů', enc_count),))] + [
            service.get_stats(self.filtering) for service in service_list(self.person)
            if service.service.include_in_reports
        ]

    def render(self, request):
        return loader.render_to_string(
            'reporting/reports/servicereport.html',
            {
                'stats': self.get_stats(),
                'filtering': self.filtering,
                'person': self.person
            },
            context_instance=RequestContext(request)
        )
