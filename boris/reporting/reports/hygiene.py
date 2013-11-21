# -*- coding: utf-8 -*-
from datetime import date, datetime, time, timedelta

from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.template.context import RequestContext
from django.db import models

from boris.clients.models import Anamnesis, RiskyManners
from boris.reporting.core import BaseReport
from boris.services.models import Encounter, IncomeExamination, Service
from boris import classification


class HygieneReport(BaseReport):
    title = u'Výstup pro hygienu'
    description = u'Souhrnný tiskový výstup pro hygienu.'
    contenttype_office = 'application/vnd.ms-word; charset=utf-8'

    def __init__(self, date_from, date_to, towns, kind):
        self.datetime_from = datetime.combine(date_from, time(0))
        self.datetime_to = datetime.combine(date_to, time(23, 59, 59))
        self.towns = towns
        self.kind = 'prevalence' if int(kind) == 1 else 'incidence'

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
        # tmp store periodicity
        p = classification.RISKY_BEHAVIOR_PERIODICITY

        # Get QuerySet of first encounters for all clients.
        encounters = Encounter.objects.first()

        # Filter encounters so that only current quarter is present.
        encounters = encounters.filter(performed_on__gte=self.datetime_from,
                                       performed_on__lt=self.datetime_to,
                                       where__in=self.towns)\
                               .annotate(first_encounter_date=models.Min('performed_on'))

        # Get client PKs from filtered encounters.
        encounter_data = {}

        for e in encounters:
            encounter_data.setdefault(e.person_id, {'first_encounter_date': date.max, 'objects': []})
            encounter_data[e.person_id]['first_encounter_date'] = min(encounter_data[e.person_id]['first_encounter_date'], e.performed_on)
            encounter_data[e.person_id]['objects'].append(e)

        # Finally, select these clients if they have anamnesis filled up.
        _a = Anamnesis.objects.filter(client__pk__in=[pk for pk in encounter_data.keys()]).select_related()
        _all = []

        # Annotate extra information needed in report.
        for a in _a:
            # Date of first encounter with client.
            a.extra_first_encounter_date = encounter_data[a.client_id]['first_encounter_date']
            # If has been cured before.
            a.extra_been_cured_before = Service.objects.filter(encounter__in=encounter_data[a.client_id]['objects'],
                                                               content_type=ContentType.objects.get_for_model(IncomeExamination)).exists()

            # When showing 'incidency', only those, who have not been cured before
            # should be returned.
            if self.kind == 'incidence' and a.extra_been_cured_before is True:
                continue

            # Information about risky behaviour and it's periodicity.
            try:
                ivrm = a.riskymanners_set.get(behavior=classification.RISKY_BEHAVIOR_KIND.INTRAVENOUS_APPLICATION)

                if (ivrm.periodicity_in_present, ivrm.periodicity_in_past) == (p.NEVER, p.NEVER):
                    a.extra_intravenous_application = 'c'
                elif ivrm.periodicity_in_present in (p.ONCE, p.OFTEN):
                    a.extra_intravenous_application = 'b'
                elif ivrm.periodicity_in_present == p.NEVER and ivrm.periodicity_in_past in (p.ONCE, p.OFTEN):
                    a.extra_intravenous_application = 'a'
                else:
                    a.extra_intravenous_application = 'd'
            except RiskyManners.DoesNotExist:
                a.extra_intravenous_application = 'd'

            # Information about syringe sharing activity.
            if a.extra_intravenous_application in ('a', 'b'):
                try:
                    ssrm = a.riskymanners_set.get(behavior=classification.RISKY_BEHAVIOR_KIND.SYRINGE_SHARING)

                    # Use current periodicity in past/current according to
                    # `extra_intravenous_application`
                    per = (ssrm.periodicity_in_present
                           if a.extra_intravenous_application == 'b'
                           else ssrm.periodicity_in_past)

                    if per in (p.ONCE, p.OFTEN):
                        a.extra_syringe_sharing = 'yes'
                    elif per == p.NEVER:
                        a.extra_syringe_sharing = 'no'
                    else:
                        a.extra_syringe_sharing = 'unknown'
                except RiskyManners.DoesNotExist:
                    a.extra_syringe_sharing = 'unknown'

            _all.append(a)

        return _all


    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'objects': self.get_anamnesis_list(),
                'datetime_from': self.datetime_from,
                'datetime_to': self.datetime_to
            },
            context_instance=RequestContext(request)
        )
