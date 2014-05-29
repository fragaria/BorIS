# -*- coding: utf-8 -*-
"""Report for the Czech Government Council for Drug Policy Coordination."""
from datetime import datetime, date, time

from django.db.models import Q, Sum
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from boris.classification import (DISEASES, DRUGS, DRUG_APPLICATION_TYPES,
    SEXES)
from boris.clients.models import Client, Anonymous
from boris.reporting.core import BaseReport
from boris.services.models import (Encounter, Address, ContactWork,
    IncomeFormFillup, IndividualCounseling, CrisisIntervention, SocialWork,
    HarmReduction, BasicMedicalTreatment, InformationService,
    IncomeExamination, DiseaseTest)
from boris.syringes.models import SyringeCollection


class GovCouncilReport(BaseReport):
    title = u'RVKPP'
    description = (u'Tiskový výstup pro Radu vlády '
        u'pro koordinaci protidrogové politiky.')

    def __init__(self, date_from, date_to, kind):
        self.datetime_from = datetime.combine(date_from, time(0))
        self.datetime_to = datetime.combine(date_to, time(23, 59, 59))
        self.kind = 'clients' if int(kind) == 1 else 'services'

    def get_filename(self):
        if self.kind == 'clients':
            return 'RVKPP_klienti.xls'
        return 'RVKPP_vykony.xls'

    # Functions used for service-related computations.

    def _get_anonymous_ids(self):
        if not hasattr(self, '_anonymous_ids'):
            self._anonymous_ids = Anonymous.objects.values_list('pk', flat=True)
        return self._anonymous_ids

    def _get_services(self, service_cls):
        filtering = {
            'encounter__performed_on__gte': self.datetime_from,
            'encounter__performed_on__lte': self.datetime_to,
        }
        return service_cls.objects.filter(**filtering)

    def _get_service_count(self, service_cls):
        """Return the number of performed services of the given class."""
        return self._get_services(service_cls).count()

    def _get_client_count(self, service_cls):
        """
        Return the number of clients with the given service.

        Anonyms are excluded.

        """
        person_ids = self._get_services(service_cls).values_list(
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
        return service_cls.objects.filter(**filtering).count()

    def _get_syringes_count(self):
        filtering = {
            'date__gte': self.datetime_from,
            'date__lte': self.datetime_to,
        }
        return SyringeCollection.objects.filter(**filtering).aggregate(Sum(
            'count'))['count__sum']

    def _get_direct_client_encounters(self):
        filtering = {
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
            'is_by_phone': False,
        }
        exclude = {'person__in': self._get_anonymous_ids()}
        return Encounter.objects.filter(**filtering).exclude(**exclude)

    def _get_phone_advice_count(self):
        encounter_ids = set()
        for cls in (SocialWork, IndividualCounseling, InformationService):
            services = self._get_services(cls)
            encounter_ids.update(services.values_list('encounter_id', flat=True))
        filtering = { # Time filtering has been performed on the services list.
            'is_by_phone': True,
            'id__in': encounter_ids,
        }
        return Encounter.objects.filter(**filtering).count()

    def _get_performed_tests_count(self, disease=None):
        filtering = {'test_execution': True}
        if disease is not None:
            filtering['disease'] = disease
        return self._get_services(DiseaseTest).filter(**filtering).count()

    def _get_tested_clients_count(self, disease=None):
        filtering = {'test_execution': True}
        if disease is not None:
            filtering['disease'] = disease
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
        encounters = Encounter.objects.filter(**filtering)
        clients = encounters.values_list('person', flat=True)
        return Client.objects.filter(pk__in=clients).exclude(primary_drug=None)

    def _get_clients_non_drug_users(self):
        """Return all sex partners and close persons from the given time period."""
        filtering = {
            'performed_on__gte': self.datetime_from,
            'performed_on__lte': self.datetime_to,
        }
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
        this_year = date.today().year
        ages = [this_year - year for year in years]
        return int(round(float(sum(ages)) / len(ages))) if ages else 0

    # <--

    def _get_data_clients(self):
        """Get data rows for the 'clients' kind."""
        drug = lambda *drugs: self._get_primary_drug_users(*drugs).count()

        non_alcohol_users = self._get_all_drug_users().exclude(
            primary_drug__in=(DRUGS.ALCOHOL, DRUGS.TOBACCO))
        alcohol_users = self._get_primary_drug_users(DRUGS.ALCOHOL)
        tobacco_users = self._get_primary_drug_users(DRUGS.TOBACCO)
        non_drug_users = self._get_clients_non_drug_users()

        return [ # (<label>, <client_count>)
            (_(u'Počet klientů s kódem – uživatelů nealkoholových drog CELKEM'),
                non_alcohol_users.count()),
            (_(u'– z toho mužů'), non_alcohol_users.filter(sex=SEXES.MALE).count()),
            (_(u'– z toho injekčních uživatelů drog'), non_alcohol_users.filter(
                primary_drug_usage__in=(DRUG_APPLICATION_TYPES.VEIN_INJECTION,
                    DRUG_APPLICATION_TYPES.MUSCLE_INJECTION)).count()),
            (_(u'– z toho se základní drogou heroin'), drug(DRUGS.HEROIN)),
            (_(u'– z toho se základní drogou buprenorfin – zneužívaný (i.v.'
                u' aplikace, černý trh)'), drug(DRUGS.SUBUTEX_LEGAL,
                    DRUGS.SUBUTEX_ILLEGAL, DRUGS.SUBOXONE)),
            (_(u'– z toho se základní drogou metadon – zneužívaný (i.v.'
                u' aplikace, černý trh)'), drug(DRUGS.METHADONE)),
            (_(u'– z toho se základní drogou pervitin'),
                drug(DRUGS.METHAMPHETAMINE)),
            (_(u'– z toho se základní drogou opiáty a/nebo pervitin'),
                drug(DRUGS.HEROIN, DRUGS.SUBUTEX_LEGAL, DRUGS.SUBUTEX_ILLEGAL,
                    DRUGS.SUBOXONE, DRUGS.METHADONE, DRUGS.METHAMPHETAMINE)),
            (_(u'Z počtu „opiáty a/nebo pervitin“ odhadované procento'
                u' polyvalentních uživatelů opiátů a pervitinu'), ''),
            (_(u'– z toho se základní drogou kokain/crack'), drug(DRUGS.COCAINE)),
            (_(u'– z toho se základní drogou kanabinoidy'), drug(DRUGS.THC)),
            (_(u'– z toho se základní drogou extáze'), drug(DRUGS.ECSTASY)),
            (_(u'– z toho se základní drogou halucinogeny'), drug(DRUGS.LSD) +
                drug(DRUGS.PSYLOCIBE)),
            (_(u'– z toho se základní drogou těkavé látky'),
                drug(DRUGS.INHALER_DRUGS)),
            (_(u'Průměrný věk klientů – uživatelů nealkoholových drog'),
                self._get_average_age(non_alcohol_users)),
            (_(u'Počet klientů – uživatelů alkoholu CELKEM'), drug(DRUGS.ALCOHOL)),
            (_(u'– z toho mužů'), alcohol_users.filter(sex=SEXES.MALE).count()),
            (_(u'Průměrný věk klientů – uživatelů alkoholu'),
                self._get_average_age(alcohol_users)),
            (_(u'Počet klientů – uživatelů tabáku CELKEM'), drug(DRUGS.TOBACCO)),
            (_(u'– z toho mužů'), tobacco_users.filter(sex=SEXES.MALE).count()),
            (_(u'Průměrný věk klientů – uživatelů tabáku'),
                self._get_average_age(tobacco_users)),
            (_(u'Počet klientů – patologických hráčů CELKEM'), 0),
            (_(u'– z toho mužů'), 0),
            (_(u'Průměrný věk klientů – patologických hráčů'), 0),
            (_(u'Odhad počtu neidentifikovaných klientů – uživatelů drog'
                u' a patologických hráčů'), 0),
            (_(u'– z toho injekčních uživatelů drog'), 0),
            (_(u'– z toho se základní drogou opiáty a/nebo pervitin'), 0),
            (_(u'Odhad počtu klientů ve zprostředkovaném kontaktu'), ''),
            (_(u'Počet klientů - neuživatelů drog, rodinných příslušníků'
                u' a blízkých osob uživatelů'), non_drug_users.count()),
            # Note that tobacco users are counted already within non alcohol users.
            (_(u'Celkový počet všech klientů'), (non_alcohol_users.count() +
                tobacco_users.count() + alcohol_users.count() +
                non_drug_users.count())),
        ]


    def _get_data_services(self):
        """Get data rows for the 'services' kind."""
        services = self._get_service_count
        clients = self._get_client_count
        anon = self._get_anonymous_count

        harm_reductions = self._get_services(HarmReduction)
        direct_client_encounters = self._get_direct_client_encounters()
        directly_encountered_clients_count = len(set(
            direct_client_encounters.values_list('person_id', flat=True)))

        return [ # (<service name>, <persons count>, <services count>)
            (_(u'Osobní kontakt s klienty'), directly_encountered_clients_count,
                direct_client_encounters.count()),
            (_(u'– z toho prvních kontaktů'), clients(IncomeExamination),
                services(IncomeExamination) - anon(IncomeExamination)),
            (_(u'Úkony potřebné pro zajištění práce s klientem'), 'xxx',
                services(Address)),
            (_(u'Kontaktní práce'), clients(ContactWork) + anon(ContactWork),
                services(ContactWork)),
            (_(u'Vstupní zhodnocení stavu klienta'), clients(IncomeFormFillup),
                services(IncomeFormFillup)),
            (_(u'Individuální poradenství'), clients(IndividualCounseling),
                services(IndividualCounseling)),
            (_(u'Individuální psychoterapie'), 0, 0),
            (_(u'Skupinové poradenství'), 0, 0),
            (_(u'Skupinová psychoterapie'), 0, 0),
            (_(u'Krizová intervence'), clients(CrisisIntervention),
                services(CrisisIntervention)),
            (_(u'Rodinná terapie'), 0, 0),
            (_(u'Skupiny pro rodiče a osoby blízké klientovi'), 0, 0),
            (_(u'Pracovní terapie'), 0, 0),
            (_(u'Sociální práce (odkazy, asistence, soc.-právní pomoc, case management)'),
                clients(SocialWork), services(SocialWork)),
            (_(u'Práce s rodinou'), 0, 0),
            (_(u'Socioterapie'), 0, 0),
            (_(u'Chráněná práce  / podporované zaměstnání'), 0, 0),
            (_(u'Psychiatrické vyšetření'), 0, 0),
            (_(u'Somatické vyšetření'), 0, 0),
            (_(u'Farmakoterapie'), 0, 0),
            (_(u'– z toho podání substituční látky'), 0, 0),
            (_(u'– z toho preskripce substituční látky'), 0, 0),
            (_(u'Základní zdravotní ošetření (vč. první pomoci, volání ZS)'),
                clients(BasicMedicalTreatment), services(BasicMedicalTreatment)),
            (_(u'Telefonické, písemné a internetové poradenství'), 'xxx',
                self._get_phone_advice_count()),
            (_(u'Korespondenční práce'), 0, 0),
            (_(u'Informační servis'), clients(InformationService),
                services(InformationService) - anon(InformationService)),
            (_(u'Edukativní program/beseda'), 0, 0),
            (_(u'Výměnný program'), clients(HarmReduction),
                services(HarmReduction)),
            (_(u'– vydané injekční jehly'), 'xxx',
                harm_reductions.aggregate(Sum('out_count'))['out_count__sum']),
            (_(u'– přijaté injekční jehly'), 'xxx',
                harm_reductions.aggregate(Sum('in_count'))['in_count__sum']),
            (_(u'– nalezené injekční jehly'), 'xxx', self._get_syringes_count()),
            (_(u'Hygienický servis'), 0, 0),
            (_(u'Potravinový servis'), 0, 0),
            (_(u'Testování na inf. nemoci'), self._get_tested_clients_count(),
                self._get_performed_tests_count()),
            (_(u'– z toho na HIV'), self._get_tested_clients_count(DISEASES.HIV),
                self._get_performed_tests_count(DISEASES.HIV)),
            (_(u'– z toho na HCV'), self._get_tested_clients_count(DISEASES.VHC),
                self._get_performed_tests_count(DISEASES.VHC)),
            (_(u'– z toho na HBV'), self._get_tested_clients_count(DISEASES.VHB),
                self._get_performed_tests_count(DISEASES.VHB)),
            (_(u'– z toho na syfilis'), self._get_tested_clients_count(
                DISEASES.SYFILIS), self._get_performed_tests_count(DISEASES.SYFILIS)),
            (_(u'Testy na přítomnost drog'), 0, 0),
            (_(u'Těhotenský test'), 0, 0),
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
            },
            context_instance=RequestContext(request)
        )
