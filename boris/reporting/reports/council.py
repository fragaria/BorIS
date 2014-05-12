# -*- coding: utf-8 -*-
"""Report for the Czech Government Council for Drug Policy Coordination."""
from datetime import datetime, time

from django.db.models import Sum
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from boris.classification import DISEASES
from boris.clients.models import Anonymous
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
        return 'vystup_pro_rvkpp.xls'

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

    def _get_data_clients(self):
        """Get data rows for the 'clients' kind.""" # TODO: implement
        return []

    def _get_data_services(self):
        """Get data rows for the 'services' kind."""
        services = self._get_service_count
        clients = self._get_client_count
        anon = self._get_anonymous_count

        harm_reductions = self._get_services(HarmReduction)
        direct_client_encounters = self._get_direct_client_encounters()
        directly_encountered_clients_count = len(set(
            direct_client_encounters.values_list('person_id', flat=True)))

        return [ # (<Service name>, <persons count>, <services count>)
            (_(u'Osobní kontakt s klienty'), directly_encountered_clients_count,
                direct_client_encounters.count()),
            (_(u'– z toho prvních kontaktů'), clients(IncomeExamination),
                services(IncomeExamination)),
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
