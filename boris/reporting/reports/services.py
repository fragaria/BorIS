# -*- coding: utf-8 -*-
from django.template import loader
from django.template.context import RequestContext

from boris.services.models import service_list
from boris.reporting.core import BaseReport


class ServiceReport(BaseReport):
    title = 'Shrnutí výkonů'
    description = 'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype = 'text/html'
    response_headers = None

    def __init__(self, date_from=None, date_to=None, town=None, person=None):
        filtering = (
            ('encounter__performed_on__gte', date_from),
            ('encounter__performed_on__lte', date_to),
            ('encounter__where', town),
            ('encounter__person', person),
        )
        filtering = ((f[0], f[1]) for f in filtering if f[1] is not None)

        self.filtering = dict(filtering)
        self.date_from = date_from
        self.date_to = date_to
        self.town = town
        self.person = person

    def get_stats(self):
        return [
            service.get_stats(self.filtering) for service in service_list()
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
