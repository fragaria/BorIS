# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from django.db.models import Q
from django.utils.translation import ugettext as _

from boris.classification import SEXES, ANONYMOUS_TYPES, DISEASES, \
    DRUG_APPLICATION_TYPES, DRUGS
from boris.clients.models import Town, District
from boris.reporting.core import Aggregation, Report, \
    SumAggregation, make_key, NonDistinctCountAggregation
from boris.reporting.models import SearchEncounter, SearchService, SearchSyringeCollection


class EncounterAggregation(Aggregation):
    model = SearchEncounter


class ServiceAggregation(Aggregation):
    model = SearchService


class AllClientEncounters(EncounterAggregation):
    title = _(u'Počet klientů')
    aggregation_dbcol = 'person'
    filtering = {'is_client': True}


class IvClientEncounters(AllClientEncounters):
    title = _(u'Z toho injekčních uživatelů drog')
    filtering = {'is_client': True, 'primary_drug_usage__in': (DRUG_APPLICATION_TYPES.VEIN_INJECTION, DRUG_APPLICATION_TYPES.MUSCLE_INJECTION),
                 'is_close_person': False}


class NonIvClientEncounters(AllClientEncounters):
    title = _(u'Z toho neinjekčních uživatelů drog')
    filtering = {'is_client': True, 'primary_drug__isnull': False,
                 'is_close_person': False}
    excludes = {'primary_drug_usage__in': (DRUG_APPLICATION_TYPES.VEIN_INJECTION, DRUG_APPLICATION_TYPES.MUSCLE_INJECTION)}


class MaleClientEncounters(AllClientEncounters):
    title = _(u'Z toho mužů')
    filtering = {'is_client': True, 'client_sex': SEXES.MALE}


class ClosePersonEncounters(AllClientEncounters):
    title = _(u'Z toho osob blízkých (rodiče, sex. partneři apod.)')
    filtering = {'is_close_person': True}


class AnonymousAggregation(NonDistinctCountAggregation, EncounterAggregation):
    title = _(u'Počet neuživatelů, kteří využili alespoň jednou služeb programu')
    aggregation_dbcol = 'person'
    filtering = {
        'is_anonymous': True,
        'person__anonymous__drug_user_type__in': (ANONYMOUS_TYPES.NON_USER,
            ANONYMOUS_TYPES.NON_USER_PARENT)
    }


class AllApproaches(ServiceAggregation, SumAggregation):
    title = _(u'Počet oslovených')
    aggregation_dbcol = 'grouping_constant'
    filtering = {'content_type_model': 'approach'}


class ApproachesDU(AllApproaches):
    title = _(u'Z toho UD')
    filtering = (
        Q(content_type_model='approach')
    ) & (
        Q(person__client__primary_drug__isnull=False) |
        Q(person__anonymous__drug_user_type__in=(ANONYMOUS_TYPES.IV,
            ANONYMOUS_TYPES.NON_IV, ANONYMOUS_TYPES.THC))
    )


class ApproachesDUTHC(AllApproaches):
    title = _(u'Z toho uživatelů THC')
    filtering = (
        Q(content_type_model='approach')
    ) & (
        Q(person__client__primary_drug__in=(DRUGS.THC,)) |
        Q(person__anonymous__drug_user_type__in=(ANONYMOUS_TYPES.THC,))
    )


class DiseaseTestBase(ServiceAggregation):
    title = _(u'Počet testů VHC')
    filtering = {
        'content_type_model': 'diseasetest',
        'service__diseasetest__disease': DISEASES.VHC
    }

disease_tests = []

for key, title in DISEASES:
    attrs = {
        'title': _(u'Počet testů %s') % title,
        'filtering': {
            'content_type_model': 'diseasetest',
            'service__diseasetest__disease': key
        }
    }
    DiseaseTestClass = type(str('DiseaseTest%s' % title), (DiseaseTestBase,), attrs)
    disease_tests.append(DiseaseTestClass)


class EncounterCount(EncounterAggregation):
    title = _(u'Počet kontaktů celkem')


class ClientEncounterCount(EncounterAggregation):
    title = _(u'z toho s klienty přímý')
    filtering = {'is_by_phone': False, 'is_client': True}


class PhoneEncounterCount(EncounterAggregation):
    title = _(u'z toho nepřímý kontakt')
    filtering = {'is_by_phone': True}


class FirstContactCount(ServiceAggregation):
    title = _(u'Počet prvních kontaktů')
    filtering = {'content_type_model': 'incomeexamination'}


class FirstContactCountDU(FirstContactCount):
    title = _(u'z toho s UD')
    filtering = (
        Q(person__client__primary_drug__isnull=False) &
        Q(person__client__close_person=False) &
        Q(content_type_model='incomeexamination')
    ) | (
        Q(person__anonymous__drug_user_type__in=(ANONYMOUS_TYPES.IV, ANONYMOUS_TYPES.NON_IV)) &
        Q(content_type_model='incomeexamination')
    )


class FirstContactCountIV(FirstContactCount):
    title = _(u'z toho nitrožilních UD')
    filtering = (
        Q(person__client__primary_drug_usage__in=(DRUG_APPLICATION_TYPES.VEIN_INJECTION,
                                                  DRUG_APPLICATION_TYPES.MUSCLE_INJECTION)) &
        Q(is_client=True) &
        Q(content_type_model='incomeexamination')
    ) | (
        Q(person__anonymous__drug_user_type=ANONYMOUS_TYPES.IV) &
        Q(content_type_model='incomeexamination')
    )


class HarmReductionCount(ServiceAggregation):
    title = _(u'Počet výměn')
    filtering = {'content_type_model': 'harmreduction'}


class GatheredSyringes(SumAggregation, ServiceAggregation):
    title = _(u'Počet přijatého inj. materiálu')
    aggregation_dbcol = 'service__harmreduction__in_count'


class IssuedSyringes(SumAggregation, ServiceAggregation):
    title = _(u'Počet vydaného inj. materiálu')
    aggregation_dbcol = 'service__harmreduction__out_count'


class SyringeCollectionCount(SumAggregation):
    title = _(u'Počet nalezených inj. stříkaček')
    aggregation_dbcol = 'count'
    model = SearchSyringeCollection


class ClientReportBase(Report):
    aggregation_classes = [
        AllClientEncounters,
        MaleClientEncounters,
        IvClientEncounters,
        NonIvClientEncounters,
        ClosePersonEncounters,
        AnonymousAggregation,
        AllApproaches,
        ApproachesDU,
        ApproachesDUTHC,
    ] + disease_tests + [
        EncounterCount,
        ClientEncounterCount,
        PhoneEncounterCount,
        FirstContactCount,
        FirstContactCountDU,
        FirstContactCountIV,
        HarmReductionCount,
        SyringeCollectionCount,
        GatheredSyringes,
        IssuedSyringes
    ]


class MonthlyStatsByTown(ClientReportBase):
    title = _(u'Měsíční')
    description = _(u'Statistika rozdělená <strong>podle měsíců</strong>. Pro '
        u'každý měsíc zobrazuje sledované informace pro jednotlivá <strong>města</strong>.')
    grouping = ('month', 'town')
    grouping_total = ('month',)

    def get_filename(self):
        return 'stat_mesicni_podle_mesta.xls'

    def _columns(self):
        if not hasattr(self, '_cols'):
            self._cols = [town for town in Town.objects.all()]
        return self._cols
    columns = property(_columns)

    def __init__(self, year, *args, **kwargs):
        self.year = year
        self.additional_filtering = {'year': year}
        super(MonthlyStatsByTown, self).__init__(*args, **kwargs)

    def months(self):
        return xrange(1, 13)

    def get_sum(self, aggregation, month):
        return aggregation.get_val(make_key((('month', month),)))

    def get_data(self):
        return [
            (month, [
                (aggregation.title, [
                    aggregation.get_val(
                        make_key((('month', month), ('town', town.pk)))
                    ) for town in self.columns
                ] + [self.get_sum(aggregation, month)]) for aggregation in self.aggregations
            ]) for month in self.months()
        ]


class StatsByTownInPeriod(ClientReportBase):
    title = _(u'Volitelné')
    description = _(u'Statistika rozdělená <strong>podle měst</strong> dle zadaného volitelného období.')
    grouping = ('town',)
    grouping_total = ('grouping_constant',)

    def __init__(self, date_from, date_to, towns):
        self.date_from = date_from
        self.date_to = date_to
        self.towns = towns or Town.objects.all()
        self.additional_filtering = {
            'performed_on__gte': date_from,
            'performed_on__lte': date_to,
            'town__in': self.towns,
        }
        super(StatsByTownInPeriod, self).__init__()

    def get_data(self):
        return [
            (aggregation.title, [
                aggregation.get_val(make_key((('town', town.pk),))) for town in self.towns
            ] + [aggregation.get_total('grouping_constant')]
            ) for aggregation in self.aggregations
        ]


class MonthlyStatsByDistrict(MonthlyStatsByTown):
    title = _(u'Okresy: měsíční')
    description = _(u'Statistika rozdělená <strong>podle měsíců</strong>. Pro '
        u'každý měsíc zobrazuje sledované informace pro jednotlivé <strong>okresy</strong>.')
    grouping = ('month', 'town__district')
    grouping_total = ('month',)

    def get_filename(self):
        return 'stat_mesicni_podle_okresu.xls'

    def _columns(self):
        if not hasattr(self, '_cols'):
            self._cols = [district for district in District.objects.all()]
        return self._cols
    columns = property(_columns)

    def get_sum(self, aggregation, month):
        return aggregation.get_val(make_key((('month', month),)))

    def get_data(self):
        return [
            (month, [
                (aggregation.title, [
                    aggregation.get_val(
                        make_key((('month', month), ('town__district', district.pk)))
                    ) for district in self.columns
                ] + [self.get_sum(aggregation, month)]) for aggregation in self.aggregations
            ]) for month in self.months()
        ]
