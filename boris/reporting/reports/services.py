# -*- coding: utf-8 -*-

from itertools import chain

from django.template import loader

from boris.services.models import service_list


class ServiceReport(object):
    title = 'Shrnutí výkonů'
    description = 'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype =  'application/vnd.ms-excel; charset=utf-8'

    def __init__(self, date_from=None, date_to=None, town=None, person=None):
        filtering = (
            ('encounter__performed_on__gte', date_from),
            ('encounter__performed_on__lte', date_to),
            ('encounter__where', town),
            ('encounter__person', person),
        )
        filtering = ((f[0], f[1]) for f in filtering if f[1] is not None)
        self.filtering = dict(filtering)

    def get_stats(self):
        stats = [
            service.get_stats(self.filtering) for service in service_list()
            if service.service.include_in_reports
        ]

        return chain(*stats)

    def render(self):
        ctx = {
            'stats': self.get_stats(),
        }
        return loader.render_to_string('reporting/reports/servicereport.html', ctx)
