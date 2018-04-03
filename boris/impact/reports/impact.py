# -*- coding: utf-8 -*-
"""Report for the Czech Government Council for Drug Policy Coordination."""
from copy import deepcopy

from datetime import datetime, date, time
from django.db.models import Count
from django.db.models import Sum
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from boris.classification import (DRUGS, RISKY_BEHAVIOR_PERIODICITY, RISKY_BEHAVIOR_KIND)
from boris.clients.models import Client, Anamnesis, RiskyManners, Town
from boris.dashboard import MONTHS_SHORT,CustomIndexDashboard
from boris.impact.core import BaseImpact
from boris.reporting.reports.council import GovCouncilReport
from boris.services.models import (Encounter, HarmReduction, IncomeExamination, Service)

_CONTENT_TYPES = {}



class ImpactReport(BaseImpact, GovCouncilReport):
    title = u'Impakt'
    description = u'Podklady pro dopadovou zprávu pro koordinaci protidrogové politiky.'

    all_towns = Town.objects.all()
    first_contact = Encounter.objects.order_by('performed_on')[0] if Encounter.objects.order_by('performed_on') else None


    def __init__(self, date_from=None, date_to=None, towns=None):
        if date_from is None:
            date_from = self.first_contact.performed_on if self.first_contact is not None else None
        if date_to:
            date_to = datetime.today()
        if towns is None:
            towns = self.all_towns
        self.datetime_from = datetime.combine(date_from, time(0))
        self.datetime_to = datetime.combine(date_to, time(23, 59, 59))
        self.towns = towns
        self.clients_in_location = self._get_all_drug_users().count()
        self.potential_clients = 6 * self.clients_in_location
        self.town_population = 10000

        GovCouncilReport.__init__(self, self.datetime_from, self.datetime_to, 1, self.towns)

        self.encounters = []
        self.persons = []
        self.syringe = []
        self.months = deepcopy(MONTHS_SHORT)

        year = datetime.today().year - 1
        month = datetime.today().month

        for i in range(12):
            month += 1
            if month == 13:
                month = 1
                year += 1

            enc_count = Encounter.objects.filter(performed_on__month=month, performed_on__year=year).count()
            person_count = Client.objects.filter(created__month=month, created__year=year).count()

            syringe_count = HarmReduction.objects.filter(encounter__performed_on__month=month,
                                                         encounter__performed_on__year=year).aggregate(
                                                            Sum('out_count')).get('out_count__sum', 0) or 0

            self.encounters.append(enc_count)
            self.persons.append(person_count)
            self.syringe.append(syringe_count)

        self.months = self.months[month:] + self.months[:month]


class ImpactTimeseries(ImpactReport):
    title = _(u'Časové řady')
    description = _(u'Časové řady')

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'date_from': self.datetime_from,
                'date_to': self.datetime_to,
                'towns': [t.title for t in self.towns],
                'encounters': self.encounters,
                'persons': self.persons,
                'syringe': self.syringe,
                'months': self.months,
                'first_contact': self.first_contact.performed_on.year,
                'clients_in_location': self.clients_in_location, 
                'potential_clients': self.potential_clients,
                'town_population': self.town_population - (7 * self.clients_in_location),
            },
            context_instance=RequestContext(request)
        )


class ImpactClient(ImpactReport):
    title = _(u'Klienti')
    description = _(u'Statistická analýza klientů')

    def get_drug_occurrence(self):
        drug = lambda *drugs: self._get_primary_drug_users(*drugs).count()
        counts_by_category = {
            'heroin': drug(DRUGS.HEROIN),
            'buprenorfin': drug(DRUGS.SUBUTEX_LEGAL, DRUGS.SUBUTEX_ILLEGAL, DRUGS.SUBOXONE),
            'metadon': drug(DRUGS.METHADONE),
            'opiáty': drug(DRUGS.VENDAL, DRUGS.RAW_OPIUM, DRUGS.BRAUN),
            'pervitin': drug(DRUGS.METHAMPHETAMINE),
            'kokain/crack': drug(DRUGS.COCAINE),
            'kanabinoidy': drug(DRUGS.THC),
            'extáze': drug(DRUGS.ECSTASY),
            'halucinogeny': drug(DRUGS.LSD, DRUGS.PSYLOCIBE),
            'těkavé látky': drug(DRUGS.INHALER_DRUGS)
        }
        return { 'labels': counts_by_category.keys(), 'values': counts_by_category.values()}

    def get_enc_distribution(self):
        bin_bounds = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 200, 300, 400]
        bin_number = len(bin_bounds)
        counts = [0] * bin_number
        bin_labels = [''] * bin_number
        client_encs = Client.objects.annotate(encounter_count=Count('encounters')).order_by('encounter_count')
        anonymous_ids = self._get_anonymous_ids()
        anonymous_encs = Encounter.objects.filter(person__in=anonymous_ids).count()
        for i in xrange(bin_number-1):
            if bin_bounds[i+1] - bin_bounds[i] == 1:
                bin_labels[i+1] = str(bin_bounds[i+1]) 
            else:
                bin_labels[i+1] = str(bin_bounds[i]+1) + '-' + str(bin_bounds[i+1])
    
            for client_enc in client_encs:
                if bin_bounds[i] < client_enc.encounter_count <= bin_bounds[i+1]:
                    counts[i] += 1
        
        return {'bounds': bin_bounds[1:bin_number], 'labels': bin_labels[1:bin_number], 'counts': counts[0:bin_number-1], 'anonymous': anonymous_encs}

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'date_from': self.datetime_from,
                'date_to': self.datetime_to,
                'towns': [t.title for t in self.towns],
                'encounters': self.encounters,
                'persons': self.persons,
                'syringe': self.syringe,
                'months': self.months,
                'first_contact': self.first_contact.performed_on.year,
                'clients_in_location': self.clients_in_location, 
                'potential_clients': self.potential_clients,
                'town_population': self.town_population-(7*self.clients_in_location),
                'drug_type_occurrence': self.get_drug_occurrence(),
                'enc_dist': self.get_enc_distribution(),
            },
            context_instance=RequestContext(request)
        )


class ImpactAnamnesis(ImpactReport):
    title = u'Anamnézy'
    description = (u'Statistický výtah z anamnéz')

    def anamnesis_dictionary(self, x):
        p = RISKY_BEHAVIOR_PERIODICITY
        return {
            p.NEVER: 'never',
            p.ONCE: 'once',
            p.OFTEN: 'often',
            p.UNKNOWN: 'unknown'               
        }.get(x, 'not found')

    def get_anamnesis_list(self):
        """
        Returns all anamnesis to report in the resulting output.

        Filters clients using following rules::
            * Client must have Anamnesis filled up
            * First recorded encounter with the client in the given year (and possibly towns)
              must be witin quarter limited by date range.
        """
        # tmp store periodicity

        p = RISKY_BEHAVIOR_PERIODICITY

        # Get QuerySet of first encounters in the given year/town for all clients.
        encounters = Encounter.objects.first(2011 and 2012 and 2013 and 2013 and 2015, towns=self.towns)
        # Filter encounters so that only the specified date range is present.
        encounters = encounters.filter(performed_on__gte=self.datetime_from,
                                       performed_on__lt=self.datetime_to)

        # Get all clients whose first encounters fall into the specified range.
        clients = encounters.values('person')

        # Now get all the encounters for these clients that fulfill the specified criteria.
        encounters = Encounter.objects.filter(performed_on__gte=self.datetime_from,
                                              performed_on__lt=self.datetime_to,
                                              where__in=self.towns,
                                              person__in=clients)

        # Get client PKs from filtered encounters.
        encounter_data = {}

        for e in encounters:
            encounter_data.setdefault(e.person_id, {'first_encounter_date': date.max, 'objects': []})
            encounter_data[e.person_id]['first_encounter_date'] = min(encounter_data[e.person_id]['first_encounter_date'], e.performed_on)
            encounter_data[e.person_id]['objects'].append(e)

        # Finally, select these clients if they have anamnesis filled up.
        _a = Anamnesis.objects.filter(client__pk__in=encounter_data.keys()).select_related()
        _all = []

        # Annotate extra information needed in report.
        for a in _a:
            # Date of first encounter with client.
            a.extra_first_encounter_date = encounter_data[a.client_id]['first_encounter_date']
            # If has been cured before - True if there is not IncomeExamination
            # within selected encounters.
            a.extra_been_cured_before = not Service.objects.filter(encounter__in=encounter_data[a.client_id]['objects'],
                                                                   content_type=IncomeExamination.real_content_type()).exists()
            # When showing 'incidency', only those, who have not been cured before
            # should be returned.
            # if self.kind == 'incidence' and a.extra_been_cured_before is True:
            if a.extra_been_cured_before is True:
                continue

            # Information about risky behaviour and it's periodicity.
            try:
                ivrm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.INTRAVENOUS_APPLICATION)

                a.iv_past = self.anamnesis_dictionary(ivrm.periodicity_in_past)
                a.iv_present = self.anamnesis_dictionary(ivrm.periodicity_in_present)

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
                a.iv_past = 'unknown'
                a.iv_present = 'unknown'

            # Information about syringe sharing activity.
            if a.extra_intravenous_application not in ('c',):
                try:
                    ssrm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.SYRINGE_SHARING)

                    # Use current periodicity in past/current according to
                    # `extra_intravenous_application`
                    a.ss_past = self.anamnesis_dictionary(ivrm.periodicity_in_past)
                    a.ss_present = self.anamnesis_dictionary(ivrm.periodicity_in_present)

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
                    a.ss_past = 'unknown'
                    a.ss_present = 'unknown'

            try:
                usrm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.SEX_WITHOUT_PROTECTION)
                a.us_past = self.anamnesis_dictionary(usrm.periodicity_in_past)
                a.us_present = self.anamnesis_dictionary(usrm.periodicity_in_present)
            except RiskyManners.DoesNotExist:
                a.us_past = 'unknown'
                a.us_present = 'unknown'
 
            try:
                rarm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.RISKY_APPLICATION)
                a.ra_past = self.anamnesis_dictionary(rarm.periodicity_in_past)
                a.ra_present = self.anamnesis_dictionary(rarm.periodicity_in_present)
            except RiskyManners.DoesNotExist:
                a.ra_past = 'unknown'
                a.ra_present = 'unknown'

            try:
                odrm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.OVERDOSING)
                a.od_past = self.anamnesis_dictionary(odrm.periodicity_in_past)
                a.od_present = self.anamnesis_dictionary(odrm.periodicity_in_present)
            except RiskyManners.DoesNotExist:
                a.od_past = 'unknown'
                a.od_present = 'unknown'

            try:
                hcrm = a.riskymanners_set.get(behavior=RISKY_BEHAVIOR_KIND.HEALTH_COMPLICATIONS)
                a.hc_past = self.anamnesis_dictionary(hcrm.periodicity_in_past)
                a.hc_present = self.anamnesis_dictionary(hcrm.periodicity_in_present)
            except RiskyManners.DoesNotExist:
                a.hc_past = 'unknown'
                a.hc_present = 'unknown'

            _all.append(a)

        return _all

    def get_anamnesis_improvements(self):
        anamnesis = self.get_anamnesis_list()

        periodicity_dict = {
            'not found': -2,
            'unknown': -1,
            'never': 0,
            'once': 1,
            'often': 2
        }

        manner_dict = {
            'iv': 'Nitrožílní aplikace',
            'ss': 'Sdílení jehel',
            'ra': 'Riziková aplikace',
            'us': 'Nechráněný sex',
            'od': 'Předávkování',
        }

        labels = []
        counts = []

        for manner in manner_dict: 
            label = ''
            improvement = 0

            manner_key_prefix = "%s" % manner 
            past_key = manner_key_prefix+'_past'
            present_key = manner_key_prefix+'_present'
            for a in anamnesis:
                past = periodicity_dict[getattr(a,past_key)]
                present = periodicity_dict[getattr(a,present_key)]              
                if present > -1 and past > -1:
                    if past > present:
                        improvement += 1
                    elif past < present:
                        improvement -= 1

            labels.append(manner_dict[manner])
            counts.append(improvement)

        data_dummy = {
                'labels': labels,
                'counts': counts,
        }
             
        return data_dummy
 
    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'date_from': self.datetime_from,
                'date_to': self.datetime_to,
                'towns': [t.title for t in self.towns],
                'encounters': self.encounters,
                'persons': self.persons,
                'syringe': self.syringe,
                'months': self.months,
                'first_contact': self.first_contact.performed_on.year,
                'clients_in_location': self.clients_in_location, 
                'anamnesis': self.get_anamnesis_list(),
                'rm_improvements': self.get_anamnesis_improvements(),
            },
            context_instance=RequestContext(request)
        )
