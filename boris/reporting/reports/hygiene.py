# -*- coding: utf-8 -*-
from datetime import date, datetime, time, timedelta

from django.template import loader
from django.template.context import RequestContext
from django.db import models

from boris.clients.models import Anamnesis
from boris.reporting.core import BaseReport
from boris.services.models import Encounter


class HygieneReport(BaseReport):
    title = u'Výstup pro hygienu'
    description = u'Souhrnný tiskový výstup pro hygienu.'
    contenttype_office = 'application/vnd.ms-word; charset=utf-8'

    def __init__(self, quarter, towns):
        self.towns = towns

        self.q_no, self.year = int(quarter.split('/')[0]), int(quarter.split('/')[1])

        df = lambda m: datetime.combine(date(self.year, m, 1), time(0))
        dt = lambda m, y=self.year: datetime.combine(date(y, m, 1), time(0)) - timedelta(seconds=1)

        if self.q_no < 4:
            self.datetime_from = df(1 + 3 * (self.q_no - 1))
            self.datetime_to = dt(4 + 3 * (self.q_no - 1))
        else:
            self.datetime_from = df(10)
            self.datetime_to = dt(1, self.year + 1)

    def get_filename(self):
        return ('vystup_pro_hygienu_%s_%s.doc' % (self.datetime_from, self.datetime_to)).replace('-', '_').replace(' ', '_')

    def get_anamnesis_list(self):
        """
        Returns all anamnesis to report in the resulting output.

        Filters clients using following rules::
            * Client must have Anamnesis filled up
            * First recorded encounter with the client must be witin quarter
              limited by date range.
        """
        # Get QuerySet of first encounters for all clients.
        encounters = Encounter.objects.first()

        # Filter encounters so that only current quarter is present.
        encounters = encounters.filter(performed_on__gte=self.datetime_from,
                                       performed_on__lt=self.datetime_to,
                                       where__in=self.towns)\
                               .annotate(first_encounter_date=models.Min('performed_on'))

        # Get client PKs from filtered encounters.
        results = encounters.values_list('person_id', 'first_encounter_date')
        encounter_dates = dict(r for r in results)

        # Finally, select these clients if they have anamnesis filled up.
        anamnesiss = Anamnesis.objects.filter(client__pk__in=[r[0] for r in results]).select_related()

        for a in anamnesiss:
            a.first_encounter_date = encounter_dates[a.client_id]

        return anamnesiss


    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'objects': self.get_anamnesis_list(),
                'q_no': self.q_no,
                'year': self.year,
                'datetime_from': self.datetime_from,
                'datetime_to': self.datetime_to
            },
            context_instance=RequestContext(request)
        )
