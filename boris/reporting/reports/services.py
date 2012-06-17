# -*- coding: utf-8 -*-

from django.template import loader

class ServiceReport(object):
    title = 'Shrnutí výkonů'
    description = 'Statistiky jednotlivých výkonů splňujících zadaná kritéria.'
    contenttype =  'application/vnd.ms-excel; charset=utf-8'

    def __init__(self, date_from, date_to):
        pass

    def render(self):
        ctx = {
        }
        return loader.render_to_string('reporting/reports/servicereport.html', ctx)
