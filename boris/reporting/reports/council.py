# -*- coding: utf-8 -*-
"""Report for the Czech Government Council for Drug Policy Coordination."""
import collections
from datetime import datetime, date, time
from django.db.models import Q, Sum
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from boris.classification import (DISEASES, DRUGS, DRUG_APPLICATION_TYPES,
    SEXES)
from boris.clients.models import Client, Anonymous
from boris.reporting.core import BaseReport
from boris.services.models import (Encounter, Approach, ContactWork,
                                   IncomeFormFillup, IndividualCounselling, CrisisIntervention, SocialWork,
                                   HarmReduction, BasicMedicalTreatment, InformationService,
                                   IncomeExamination, DiseaseTest, HygienicService, FoodService,
                                   Therapy, PostUsage, UrineTest, GroupCounselling, WorkWithFamily,
                                   UtilityWork, AsistService, Service, service_list, TimeDotation,
                                   SUBSERVICES_AGGREGATION_NO_SUBSERVICES)
from boris.syringes.models import SyringeCollection

_SERVICES = {}


def get_indirect_services():
    # 'indirect' services done by phone are counted as IndirectService in regards to time dotations
    if 'indirect' not in _SERVICES:
        _SERVICES['indirect'] = [
            SocialWork, IndividualCounselling, InformationService
        ]
    return _SERVICES['indirect']


class GovCouncilReport(BaseReport):
    title = u'RVKPP'
    description = (u'Tiskový výstup pro Radu vlády '
        u'pro koordinaci protidrogové politiky.')

    def __init__(self, date_from, date_to, kind, towns):
        self.datetime_from = datetime.combine(date_from, time(0))
        self.datetime_to = datetime.combine(date_to, time(23, 59, 59))
        self.kind = 'clients' if int(kind) == 1 else 'services'
        self.towns = towns

    def get_filename(self):
        if self.kind == 'clients':
            return 'RVKPP_klienti.xls'
        return 'RVKPP_vykony.xls'

    # Functions used for service-related computations.

    def _get_anonymous_ids(self):
        if not hasattr(self, '_anonymous_ids'):
            self._anonymous_ids = Anonymous.objects.values_list('pk', flat=True)
        return self._anonymous_ids

    def _get_services(self, service_cls, extra_filtering=None):
        filtering = self.__default_service_filtering()
        if extra_filtering is not None:
            filtering.update(extra_filtering)
        return service_cls.objects.filter(**filtering)

    def get_number_of_approached_count(self):
        filtering = self.__default_service_filtering()
        count = Approach._get_stats(filtering)[0][1]
        return count

    def _get_service_count(self, service_classes, extra_filtering=None):
        """Return the number of performed services of the given class."""
        if not isinstance(service_classes, collections.Iterable):
            service_classes = [service_classes]
        res = 0
        for service_cls in service_classes:
            res += self._get_services(service_cls, extra_filtering=extra_filtering).count()
        return res

    def _get_service_count_all(self):
        """Return the number of all performed services and subservices."""
        filtering = self.__default_service_filtering()
        indirect_content_types = get_indirect_services()
        total_count = 0
        # prevents double-counting of a service
        content_types = []
        for service in self._get_services(Service):
            content_type = service.content_type
            if content_type not in content_types:
                subservices = service.cast().get_stats(filtering, only_subservices=True, only_basic=True)[1]
                subservices_count = sum([list(s)[1] for s in subservices])
                if service.encounter.is_by_phone and service in indirect_content_types:
                    total_count += subservices_count
                elif hasattr(service.Options, 'agg_type') and service.Options.agg_type == SUBSERVICES_AGGREGATION_NO_SUBSERVICES:
                    total_count += 1
                else:
                    total_count += subservices_count
                content_types.append(content_type)
        return total_count

    def get_direct_subservice_count(self, service_classes):
        return self._get_subservice_count(service_classes, extra_filtering={'encounter__is_by_phone': False})

    def _get_subservice_count(self, service_classes, extra_filtering=None):
        """Return the number of performed subservices of the given class.
        This is used when count of services should be in fact sum of selected subservices"""
        if not isinstance(service_classes, collections.Iterable):
            service_classes = [service_classes]
        filtering = self.__default_service_filtering()
        if extra_filtering is not None:
            filtering.update(extra_filtering)
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
        filtering = self.__default_service_filtering()
        filtering.update({
            'encounter__person__in': anonymous_ids,
        })
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
        filtering = self.__default_encounter_filtering(filtering)
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
        filtering = self.__default_encounter_filtering()
        encounters = Encounter.objects.filter(**filtering)
        clients = encounters.values_list('person', flat=True)
        return Client.objects.filter(pk__in=clients, close_person=False, sex_partner=False).exclude(primary_drug=None)

    def _get_clients_non_drug_users(self):
        """Return all sex partners and close persons from the given time period."""
        filtering = self.__default_encounter_filtering()
        encounters = Encounter.objects.filter(**filtering)
        clients = encounters.values_list('person', flat=True)
        return Client.objects.filter(pk__in=clients).filter(
            Q(close_person=True) | Q(sex_partner=True))

    def _get_primary_drug_users(self, *drugs):
        """Return all clients with primary drugs from the given ones."""
        clients = self._get_all_drug_users()
        return clients.filter(primary_drug__in=drugs)

    def _get_average_age(self, clients):
        """Get the average age of the input clients."""
        years = [c.birthdate.year for c in clients if c.birthdate]
        this_year = self.datetime_to.year or date.today().year
        ages = [this_year - year for year in years]
        return int(round(float(sum(ages)) / len(ages))) if ages else 0

    def _get_services_time(self):
        services = [service for service in service_list()
                    if service.service.include_in_reports]
        filtering = self.__default_service_filtering()

        total_time_spent = 0
        for service in services:
            enc_ids = service.objects.filter(**filtering).values_list('encounter__id', flat=True)
            total_time_spent += TimeDotation.time_spent_on_encounters(enc_ids, service)
        return total_time_spent

    def __default_service_filtering(self, filtering=None):
        if filtering is None:
            filtering = {}
        filtering.update({
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        })
        if self.towns:
            filtering['encounter__where__in'] = self.towns
        return filtering

    def __default_encounter_filtering(self, filtering=None):
        if filtering is None:
            filtering = {}
        filtering.update({
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
        })
        if self.towns:
            filtering['where__in'] = self.towns
        return filtering

    # <--

    def _get_data_clients(self):
        """Get data rows for the 'clients' kind."""
        drug = lambda *drugs: self._get_primary_drug_users(*drugs).count()
        non_alcohol_users = self._get_all_drug_users().exclude(
            primary_drug__in=(
            DRUGS.ALCOHOL, DRUGS.TOBACCO, DRUGS.PATHOLOGICAL_GAMBLING, DRUGS.OTHER_NON_SUBSTANCE_ADDICTION))
        alcohol_users = self._get_primary_drug_users(DRUGS.ALCOHOL)
        tobacco_users = self._get_primary_drug_users(DRUGS.TOBACCO)
        non_drug_users = self._get_clients_non_drug_users()
        non_substance_users = self._get_primary_drug_users(DRUGS.PATHOLOGICAL_GAMBLING,
                                                           DRUGS.OTHER_NON_SUBSTANCE_ADDICTION)

        return [  # (<id>, <label>, <client_count>)
            (_(u'skupina 1'), _(u'Klienti - uživatelé drog, kromě alkoholu (sk. 2) a tabáku (sk. 3)'), u''),
            (_(u'1.1'), _(u'základní droga heroin'), drug(DRUGS.HEROIN)),
            (_(u'1.2'), _(
                u'základní droga buprenorfin - zneužívaný (non lege artis, injekčně, bez indikace lékařem, z černého trhu atd.)'),
             drug(DRUGS.SUBUTEX_LEGAL, DRUGS.SUBUTEX_ILLEGAL, DRUGS.SUBOXONE)),
            (_(u'1.3'), _(
                u'základní droga metadon - zneužívaný (non lege artis, injekčně, bez indikace lékařem, z černého trhu atd.)'),
             drug(DRUGS.METHADONE)),
            (_(u'1.4'), _(u'základní droga jiné opiáty (opium, morfium, fentanyl, tramadol etc.)'),
             drug(DRUGS.VENDAL, DRUGS.RAW_OPIUM, DRUGS.BRAUN, DRUGS.FENTANYL)),
            (_(u'1.5'), _(u'základní droga pervitin'), drug(DRUGS.METHAMPHETAMINE)),
            (_(u'1.6'), _(u'základní droga kokain/crack'), drug(DRUGS.COCAINE)),
            (_(u'1.7'), _(u'základní droga kanabinoidy'), drug(DRUGS.THC)),
            (_(u'1.8'), _(u'základní droga extáze'), drug(DRUGS.ECSTASY)),
            (_(u'1.9'), _(u'základní droga halucinogeny'), drug(DRUGS.LSD, DRUGS.PSYLOCIBE)),
            (_(u'1.10'), _(u'základní droga těkavé látky'), drug(DRUGS.INHALER_DRUGS)),
            (_(u'1.11'), _(u'jiná základní droga, kromě alkoholu a tabáku'),
             drug(DRUGS.DESIGNER_DRUGS, DRUGS.MEDICAMENTS)),
            (_(u'1.12'), _(u'celkem klientů - uživatelů drog '), non_alcohol_users.count()),
            (_(u'1.12.1'), _(u'z toho mužů'), non_alcohol_users.filter(sex=SEXES.MALE).count()),
            (_(u'1.12.2'), _(u'z toho injekčních uživatelů drog'), non_alcohol_users.filter(
                primary_drug_usage__in=(DRUG_APPLICATION_TYPES.VEIN_INJECTION,
                                        DRUG_APPLICATION_TYPES.MUSCLE_INJECTION)).count()),
            (_(u'1.13'), _(u'průměrný věk klientů - uživatelů drog'), self._get_average_age(non_alcohol_users)),

            (_(u'skupina 2'), _(u'Klienti se základní drogou alkohol'), u''),
            (_(u'2.1'), _(u'celkem klientů se základní drogou alkohol'), alcohol_users.count()),
            (_(u'2.1.1'), _(u'z toho mužů'), alcohol_users.filter(sex=SEXES.MALE).count()),
            (_(u'2.2'), _(u'průměrný věk klientů se základní drogou alkohol'), self._get_average_age(alcohol_users)),

            (_(u'skupina 3'), _(u'Klienti se základní drogou tabák'), u''),
            (_(u'3.1'), _(u'celkem klientů se základní drogou tabák'), tobacco_users.count()),
            (_(u'3.1.1'), _(u'z toho mužů'), tobacco_users.filter(sex=SEXES.MALE).count()),
            (_(u'3.2'), _(u'průměrný věk klientů se základní drogou tabák'), self._get_average_age(tobacco_users)),

            (_(u'skupina 4'), _(u'Klienti s diagnózou z oblasti nelátkových závislostí'), u''),
            (_(u'4.1'), _(u'počet klientů s diagnózou patologické hráčství'),
             drug(DRUGS.PATHOLOGICAL_GAMBLING)),
            (_(u'4.2'), _(u'počet klientů s jinou nelátkovou závislostí'),
             drug(DRUGS.OTHER_NON_SUBSTANCE_ADDICTION)),
            (_(u'4.3'), _(u'celkem klientů s diagnózou z oblasti nelátkových závislostí'),
             non_substance_users.count()),
            (_(u'4.3.1'), _(u'z toho mužů'),
             non_substance_users.filter(sex=SEXES.MALE).count()),
            (_(u'4.4'), _(u'průměrný věk klientů s diagnózou z oblasti nelátkových závislostí'),
             self._get_average_age(non_substance_users)),

            (_(u'skupina 5'), _(u'Identifikovaní klienti programu celkem'), u''),
            (_(u'5.1'), _(u'Celkem  všech klientů, uživatelů'),
             self._get_all_drug_users().count()),
            (_(u'5.1.1'), _(u'z toho prvních kontaktů'), self._get_client_count(IncomeExamination)),
            (_(u'5.2'),
             _(u'Celkem ostatních klientů (neuživatelé, rodinní příslušníci, blízcí osob se závislostním problémem)'),
             non_drug_users.count()),
            (_(u'5.3'), _(u'Celkem všech klientů (uživatelů i neuživatelů)'),
             non_drug_users.count() + self._get_all_drug_users().count()),

            (_(u'skupina 6'), _(u'Neidentifikovaní klienti'), u''),
            (_(u'6.1'), _(u'odhad počtu neidentifikovaných klientů se základní drogou opiáty'), u''),
            (_(u'6.2'), _(u'odhad počtu neidentifikovaných klientů s základní drogou pervitin'), u''),
            (_(u'6.3'), _(u'odhad počtu neidentifikovaných klientů - injekčních uživatelů drog'), u''),

            (_(u'skupina 7'), _(u'Klienti ve zprostředkovaném kontaktu'), u''),
            (_(u'7.1'), _(u'Odhad počtu klientů ve zprostředkovaném kontaktu'), u''),
        ]

    def _get_data_services(self):
        """Get data rows for the 'services' kind."""
        services = self._get_service_count
        subservices = self._get_subservice_count
        clients = self._get_client_count
        anon = self._get_anonymous_count

        harm_reductions = self._get_services(HarmReduction)
        direct_client_encounters = self._get_direct_client_encounters()
        phone_client_encounters = self._get_phone_client_encounters()
        directly_encountered_client_ids = set(direct_client_encounters.values_list('person_id', flat=True))
        phone_encountered_client_ids = set(phone_client_encounters.values_list('person_id', flat=True))
        directly_encountered_clients_count = len(directly_encountered_client_ids)
        phone_encountered_clients_count = len(phone_encountered_client_ids)

        pregnancy_test_services = self._get_services(UrineTest).filter(pregnancy_test=True)
        drug_test_services = self._get_services(UrineTest).filter(drug_test=True)

        return [ # (<service name>, <persons count>, <services count>)
            (_(u'Celkový počet přímých kontaktů s klienty'),
             directly_encountered_clients_count, direct_client_encounters.count()),
            (_(u'Celkový počet nepřímých kontaktů s identifikovanými klienty'),
             phone_encountered_clients_count, phone_client_encounters.count()),
            (_(u'Úkony potřebné pro zajištění přímé práce s klientem'),
             'xxx', self.get_number_of_approached_count()),
            (_(u'Kontaktní práce'),
             clients(ContactWork) + anon(ContactWork), services(ContactWork)),
            (_(u'Vstupní zhodnocení stavu klienta'),
             clients(IncomeFormFillup), services(IncomeFormFillup)),
            (_(u'Individuální poradenství'),
             self._get_direct_client_count(IndividualCounselling), self.get_direct_subservice_count(IndividualCounselling)),
            (_(u'Individuální psychoterapie'),
             '', ''),
            (_(u'Skupinové poradenství'),
             clients(GroupCounselling), services(GroupCounselling)),
            (_(u'Skupinová psychoterapie'),
             '', ''),
            (_(u'Krizová intervence'),
             clients(CrisisIntervention), services(CrisisIntervention)),
            (_(u'Rodinná terapie'),
             '', ''),
            (_(u'Skupiny pro rodiče a osoby blízké klientovi'),
             '', ''),
            (_(u'Pracovní terapie'),
             clients(Therapy), services(Therapy)),
            (_(u'Sociální práce (odkazy, asistence, soc.-právní pomoc, case management)'),
             self._get_direct_client_count(SocialWork) + clients([AsistService, UtilityWork]), services([AsistService]) + self.get_direct_subservice_count(SocialWork) + subservices(UtilityWork)),
            (_(u'Práce s rodinou'),
             clients(WorkWithFamily), services(WorkWithFamily)),
            (_(u'Socioterapie'),
             '', ''),
            (_(u'Chráněná práce  / podporované zaměstnání'),
             '', ''),
            (_(u'Psychiatrické vyšetření'),
             '', ''),
            (_(u'Somatické vyšetření'),
             '', ''),
            (_(u'Farmakoterapie'),
             '', ''),
            (_(u'- z toho podání substituční látky'),
             '', ''),
            (_(u'- z toho preskripce substituční látky'),
             '', ''),
            (_(u'Základní zdravotní ošetření (vč. první pomoci)'),
             clients(BasicMedicalTreatment), services(BasicMedicalTreatment)),
            (_(u'Telefonické, písemné a internetové poradenství'),
             'xxx', self._get_phone_advice_count()),
            (_(u'Korespondenční práce'),
             clients(PostUsage), services(PostUsage)),
            (_(u'Informační servis'),
             self._get_direct_client_count(InformationService), self.get_direct_subservice_count(InformationService)),
            (_(u'Edukativní program/beseda'),
             '', ''),
            (_(u'Distribuce harm reduction materiálu'),
             clients(HarmReduction), services(HarmReduction)),
            (_(u'Počet vydaných injekčních jehel a stříkaček (ks)'),
             'xxx', harm_reductions.aggregate(Sum('out_count'))['out_count__sum']),
            (_(u'Počet přijatých injekčních jehel a stříkaček (ks)'),
             'xxx', harm_reductions.aggregate(Sum('in_count'))['in_count__sum']),
            (_(u'Počet nalezených injekčních jehel a stříkaček (ks)'),
             'xxx', self._get_syringes_count()),
            (_(u'Hygienický servis'),
             clients(HygienicService), subservices(HygienicService)),
            (_(u'Potravinový servis'),
             clients(FoodService), services(FoodService)),
            (_(u'Testování na inf. nemoci'),
             clients(DiseaseTest), subservices(DiseaseTest)),
            (_(u'– z toho na HIV'),
             self._get_tested_clients_count(DISEASES.HIV), self._get_performed_tests_count(DISEASES.HIV)),
            (_(u'– z toho na HCV'),
             self._get_tested_clients_count(DISEASES.VHC), self._get_performed_tests_count(DISEASES.VHC)),
            (_(u'– z toho na HBV'),
             self._get_tested_clients_count(DISEASES.VHB), self._get_performed_tests_count(DISEASES.VHB)),
            (_(u'– z toho na syfilis'),
             self._get_tested_clients_count(DISEASES.SYFILIS), self._get_performed_tests_count(DISEASES.SYFILIS)),
            (_(u'Orientační test z moči na přítomnost drog'),
             self._get_queryset_client_count(drug_test_services), drug_test_services.count()),
            (_(u'Orientační test z moči - těhotenský test'),
             self._get_queryset_client_count(pregnancy_test_services), pregnancy_test_services.count()),
            (_(u'Vyšetření adiktologem při zahájení adiktologické péče (38021)'),
             '', ''),
            (_(u'Vyšetření adiktologem kontrolní (39022)'),
             '', ''),
            (_(u'Minimální kontakt adiktologa s pacientem (38023)'),
             '', ''),
            (_(u'Adiktologická terapie individuální (38024)'),
             '', ''),
            (_(u'Adiktologická terapie rodinná (38025)'),
             '', ''),
            (_(u'Adiktologická terapie skupinová, typ I. pro skupinu max. 9 osob (38026)'),
             '', ''),
            (_(u'Celkový počet/čas všech poskytnutných výkonů (hod)'),
             u'', '%s / %.2f' % (self._get_service_count_all(), float(self._get_services_time()) / 60.0)),
        ]

    def get_data(self):
        """Returns the data table based on the subtype of the report."""
        if self.kind == 'clients':
            return self._get_data_clients()
        else:
            return self._get_data_services()

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            {
                'rows': self.get_data(),
                'date_from': self.datetime_from,
                'date_to': self.datetime_to,
                'report_kind': self.kind,
                'towns': [t.title for t in self.towns],
            },
            context_instance=RequestContext(request)
        )
