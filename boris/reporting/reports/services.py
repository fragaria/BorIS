# -*- coding: utf-8 -*-

from django.template import loader

from boris.services.models import service_list


class ServiceReport(object):
    title = 'Shrnutí výkonů'
    description = 'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype =  'application/vnd.ms-excel; charset=utf-8'

    def __init__(self, date_from=None, date_to=None):
        self.date_from = date_from
        self.date_to = date_to

    def get_stats(self):
        mapping = {
            self.date_to: 'encounter__performed_on__lte',
        }
        filtering = {}
        for key in mapping:
            if key:
                filtering[mapping[key]] = key

        return (
            service.get_stats(filtering) for service in service_list()
            if service.service.include_in_reports
        )

    def render(self):
        ctx = {
            'stats': self.get_stats(),
        }
        return loader.render_to_string('reporting/reports/servicereport.html', ctx)
