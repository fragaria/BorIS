# -*- coding: utf-8 -*-
"""Report for the Czech Government Council for Drug Policy Coordination."""
import collections
from django.db.models import F, Count
from datetime import datetime, date, time
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from boris.classification import (DISEASES, DRUGS, DRUG_APPLICATION_TYPES,
    SEXES, RISKY_BEHAVIOR_PERIODICITY, RISKY_BEHAVIOR_KIND)
from boris.clients.models import Client, Anonymous, Anamnesis, RiskyManners, PractitionerContact, GroupContact, TerrainNotes, Town 
from boris.impact.core import BaseReport
from boris.services.models import (Encounter, Address, Approach, ContactWork,
                                   IncomeFormFillup, IndividualCounselling, CrisisIntervention, SocialWork,
                                   HarmReduction, BasicMedicalTreatment, InformationService,
                                   IncomeExamination, DiseaseTest, HygienicService, FoodService,
                                   WorkTherapy, PostUsage, UrineTest, GroupCounselling, WorkWithFamily,
                                   WorkTherapyMeeting, UtilityWork, AsistService, Service)
from boris.syringes.models import SyringeCollection
import json
from django.core.serializers.json import DjangoJSONEncoder 


_CONTENT_TYPES = {}


def get_indirect_content_types():
    if 'indirect' not in _CONTENT_TYPES:
        _CONTENT_TYPES['indirect'] = [
            ContentType.objects.get_for_model(cls)
            for cls in (SocialWork, IndividualCounselling, InformationService)
        ]
    return _CONTENT_TYPES['indirect']


def get_no_subservice_content_types():
    if 'no_subservice' not in _CONTENT_TYPES:
        _CONTENT_TYPES['no_subservice'] = [
            ContentType.objects.get_for_model(cls) for cls in (HarmReduction,)
        ]
    return _CONTENT_TYPES['no_subservice']


class ImpactReport(BaseReport):
    title = u'Impakt'
    description = (u'Podklady pro dopadovou zprávu '
        u'pro koordinaci protidrogové politiky.')

    all_towns = Town.objects.all()
    first_contact = Encounter.objects.order_by('performed_on')[0] if Encounter.objects.order_by('performed_on') else None


    def __init__(self, date_from = (first_contact.performed_on if first_contact != None else None), date_to = datetime.today(), towns = all_towns):
        self.datetime_from = datetime.combine(date_from, time(0))
        self.datetime_to = datetime.combine(date_to, time(23, 59, 59))
        self.towns = towns
        self.clients_in_location = self._get_all_drug_users().count()
        self.potential_clients = 6*self.clients_in_location
        self.town_population = 10000 

        # self.first_contact = first_contact

        if(self.first_contact != None):
            number_of_months = (datetime.today().year - self.first_contact.performed_on.year)*12 + datetime.today().month - self.first_contact.performed_on.month 
            year = self.first_contact.performed_on.year
            month = self.first_contact.performed_on.month
        else:
            number_of_months =12
            year = datetime.today().year - 3
            month = datetime.today().month

        self.encounters = []
        self.persons = []
        self.syringe = []
        self.months = ['Led', 'Úno', 'Bře', 'Dub', 'Kvě', 'Črv', 'Črn', 'Srp', 'Zář', 'Říj', 'Lis', 'Pro']

        for i in range(number_of_months):
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


    def _get_anonymous_ids(self):
        if not hasattr(self, '_anonymous_ids'):
            self._anonymous_ids = Anonymous.objects.values_list('pk', flat=True)
        return self._anonymous_ids

    def _get_services(self, service_cls, extra_filtering=None):
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        }
        if extra_filtering is not None:
            filtering.update(extra_filtering)
        if self.towns:
            filtering['encounter__where__in'] = self.towns
        return service_cls.objects.filter(**filtering)

    def _get_service_count(self, service_classes, extra_filtering=None):
        """Return the number of performed services of the given class."""
        if not isinstance(service_classes, collections.Iterable):
            service_classes = [service_classes]
        res = 0
        for service_cls in service_classes:
            res += self._get_services(service_cls, extra_filtering=extra_filtering).count()
        return res

    def get_direct_subservice_count(self, service_classes):
        return self._get_subservice_count(service_classes, extra_filtering={'encounter__is_by_phone': False})

    def _get_subservice_count(self, service_classes, extra_filtering=None):
        """Return the number of performed subservices of the given class.
        This is used when count of services should be in fact sum of selected subservices"""
        if not isinstance(service_classes, collections.Iterable):
            service_classes = [service_classes]
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        }
        if extra_filtering is not None:
            filtering.update(extra_filtering)
        if self.towns:
            filtering['encounter__where__in'] = self.towns
        res = 0
        for service_cls in service_classes:
            stats = service_cls.get_stats(filtering, only_subservices=True, only_basic=True)[1]
            res += sum([stat[1] for stat in stats])
        return res

    def _get_client_count(self, service_classes, extra_filtering=None):
        """
        Return the number of clients with the given service.

        Anonyms are excluded.

        """
        if not isinstance(service_classes, collections.Iterable):
            service_classes = [service_classes]
        person_ids = []
        for service_cls in service_classes:
            person_ids += self._get_services(service_cls, extra_filtering=extra_filtering).values_list(
                'encounter__person_id', flat=True)
        anonymous_ids = self._get_anonymous_ids()
        return len(set(person_ids) - set(anonymous_ids))

    def _get_direct_client_count(self, service_classes):
        return self._get_client_count(service_classes, extra_filtering={'encounter__is_by_phone': False})

    def _get_queryset_client_count(self, qs):
        """
        Return the number of clients in the given Service queryset.

        Anonyms are excluded.

        """
        person_ids = qs.values_list(
            'encounter__person_id', flat=True)
        anonymous_ids = self._get_anonymous_ids()
        return len(set(person_ids) - set(anonymous_ids))

    def _get_anonymous_count(self, service_cls):
        """Return number of services of the given class performed by anonyms."""
        anonymous_ids = self._get_anonymous_ids()
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
            'encounter__person__in': anonymous_ids,
        }
        if self.towns:
            filtering['encounter__where__in'] = self.towns
        return service_cls.objects.filter(**filtering).count()

    def _get_syringes_count(self):
        filtering = {
            'date__gte': self.datetime_from,
            'date__lte': self.datetime_to,
        }
        if self.towns:
            filtering['town__in'] = self.towns
        return SyringeCollection.objects.filter(**filtering).aggregate(Sum(
            'count'))['count__sum']

    def _get_direct_client_encounters(self):
        return self.__get_client_encounters({'is_by_phone': False})

    def _get_phone_client_encounters(self):
        return self.__get_client_encounters({'is_by_phone': True})

    def __get_client_encounters(self, filtering):
        filtering.update({
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
        })
        if self.towns:
            filtering['where__in'] = self.towns
        exclude = {'person__in': self._get_anonymous_ids()}
        return Encounter.objects.filter(**filtering).exclude(**exclude)

    def _get_phone_advice_count(self):
        sum = 0
        for cls in (SocialWork, IndividualCounselling, InformationService):
            filtering = {
                'encounter__is_by_phone': True,
            }
            sum += self._get_subservice_count(cls, extra_filtering=filtering)
        return sum

    def _get_performed_tests_count(self, disease):
        filtering = {'disease': disease}
        return self._get_services(DiseaseTest).filter(**filtering).count()

    def _get_tested_clients_count(self, disease):
        filtering = {'disease': disease}
        person_ids = self._get_services(DiseaseTest).filter(
            **filtering).values_list('encounter__person_id', flat=True)
        anonymous_ids = self._get_anonymous_ids()
        return len(set(person_ids) - set(anonymous_ids))

    # <--

    # Functions used for client-related computations

    def _get_all_drug_users(self):
        """Return all non-anonymous drug users from the given time period."""
        filtering = {
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
        }
        if self.towns:
            filtering['where__in'] = self.towns
        encounters = Encounter.objects.filter(**filtering)
        clients = encounters.values_list('person', flat=True)
        return Client.objects.filter(pk__in=clients, close_person=False, sex_partner=False).exclude(primary_drug=None)

    def _get_clients_non_drug_users(self):
        """Return all sex partners and close persons from the given time period."""
        filtering = {
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
        }
        if self.towns:
            filtering['where__in'] = self.towns
        encounters = Encounter.objects.filter(**filtering)
        clients = encounters.values_list('person', flat=True)
        return Client.objects.filter(pk__in=clients).filter(
            Q(close_person=True) | Q(sex_partner=True))

    def _get_primary_drug_users(self, *drugs):
        """Return all clients with primary drugs from the given ones."""
        clients = self._get_all_drug_users()
        return clients.filter(primary_drug__in=drugs)

    def _get_services_time(self):
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        }
        if self.towns:
            filtering['encounter__where__in'] = self.towns
        sum = 0
        content_types = []
        for service in self._get_services(Service):
            # prevent double count in case of same service class being multiple on one encounter
            if service.content_type not in content_types:
                sum += service.get_time_spent(filtering, get_indirect_content_types(), get_no_subservice_content_types())
                content_types.append(service.content_type)
        return sum

    def get_data(self):
        """Returns the data table based on the subtype of the report."""
        return self._get_data_clients()

class ImpactTimeseries(ImpactReport):
    title = u'Časové řady'
    description = (u'Časové řady ')

    # <--
    def get_drug_occurrence(self):
        drug = lambda *drugs: self._get_primary_drug_users(*drugs).count()
        counts_by_category = {
            'heroin' : drug(DRUGS.HEROIN),
            'buprenorfin' : drug(DRUGS.SUBUTEX_LEGAL, DRUGS.SUBUTEX_ILLEGAL, DRUGS.SUBOXONE),
            'metadon' : drug(DRUGS.METHADONE),
            'opiáty' : drug(DRUGS.VENDAL, DRUGS.RAW_OPIUM, DRUGS.BRAUN),
            'pervitin' : drug(DRUGS.METHAMPHETAMINE),
            'kokain/crack': drug(DRUGS.COCAINE),
            'kanabinoidy' : drug(DRUGS.THC),
            'extáze' : drug(DRUGS.ECSTASY),
            'halucinogeny' : drug(DRUGS.LSD, DRUGS.PSYLOCIBE),
            'těkavé látky' : drug(DRUGS.INHALER_DRUGS)
        }
        return { 'labels': counts_by_category.keys(), 'values' : counts_by_category.values()}


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
                'clients_in_location' : self.clients_in_location, 
                'potential_clients' : self.potential_clients,
                'town_population' : self.town_population-(7*self.clients_in_location),
            },
            context_instance=RequestContext(request)
        )


class ImpactClient(ImpactReport):
    title = u'Klienti'
    description = (u'Statistická analýza klientů')

    # <--
    def get_drug_occurrence(self):
        drug = lambda *drugs: self._get_primary_drug_users(*drugs).count()
        counts_by_category = {
            'heroin' : drug(DRUGS.HEROIN),
            'buprenorfin' : drug(DRUGS.SUBUTEX_LEGAL, DRUGS.SUBUTEX_ILLEGAL, DRUGS.SUBOXONE),
            'metadon' : drug(DRUGS.METHADONE),
            'opiáty' : drug(DRUGS.VENDAL, DRUGS.RAW_OPIUM, DRUGS.BRAUN),
            'pervitin' : drug(DRUGS.METHAMPHETAMINE),
            'kokain/crack': drug(DRUGS.COCAINE),
            'kanabinoidy' : drug(DRUGS.THC),
            'extáze' : drug(DRUGS.ECSTASY),
            'halucinogeny' : drug(DRUGS.LSD, DRUGS.PSYLOCIBE),
            'těkavé látky' : drug(DRUGS.INHALER_DRUGS)
        }
        return { 'labels': counts_by_category.keys(), 'values' : counts_by_category.values()}

    def get_enc_distribution(self):
        bin_bounds = [0,1,2,3,4,5,10,20,30, 40, 50,100,200,300,400]
        bin_number = len(bin_bounds)
        counts = [0] * bin_number
        bin_labels = [''] * bin_number
        client_encs = Client.objects.annotate(encounter_count=Count('encounters')).order_by('encounter_count')
        anonymous_ids = self._get_anonymous_ids()
        anonymous_encs = Encounter.objects.filter(person__in=anonymous_ids).count()
        for i in xrange(bin_number-1):
            if(bin_bounds[i+1]-bin_bounds[i] == 1):
                bin_labels[i+1] = str(bin_bounds[i+1]) 
            else:
                bin_labels[i+1] = str(bin_bounds[i]+1)+'-'+str(bin_bounds[i+1]) 
    
            for client_enc in client_encs:
                if (client_enc.encounter_count > bin_bounds[i] and client_enc.encounter_count <= bin_bounds[i+1]):
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
                'clients_in_location' : self.clients_in_location, 
                'potential_clients' : self.potential_clients,
                'town_population' : self.town_population-(7*self.clients_in_location),
                'drug_type_occurrence' : self.get_drug_occurrence(),
                'enc_dist' : self.get_enc_distribution(),
            },
            context_instance=RequestContext(request)
        )


class ImpactAnamnesis(ImpactReport):
    title = u'Anamnézy'
    description = (u'Statistický výtah z anamnéz')

    def anamnesis_dictionary(self, x):
        p = RISKY_BEHAVIOR_PERIODICITY
        return {
            p.NEVER : 'never',
            p.ONCE : 'once',
            p.OFTEN : 'often',
            p.UNKNOWN : 'unknown'               
        }.get(x, 'not found')

    def get_number_of_addressed_count(self):
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        }
        if self.towns:
            filtering['encounter__where__in'] = self.towns

        approaches = Approach.objects.filter(**filtering)
        count = 0
        for a in approaches:
            count += a.number_of_addressed

        return count

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
            #if self.kind == 'incidence' and a.extra_been_cured_before is True:
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
            if a.extra_intravenous_application not in ('c'):
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
                'clients_in_location' : self.clients_in_location, 
                'anamnesis' : self.get_anamnesis_list(),
          },
            context_instance=RequestContext(request)
        )
