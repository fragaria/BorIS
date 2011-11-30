# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from boris.classification import SEXES
from boris.clients.models import Town
from boris.reporting.core import AggregationRow, Report,\
    SumAggregationRow, hashdict
from boris.reporting.models import SearchEncounter

class AllEncounters(AggregationRow):
    title = u'Počet klientů'
    model = SearchEncounter
    aggregation_dbcol = 'person'


class MaleEncounters(AllEncounters):
    title = u'Z toho mužů'
    filtering = {'client_sex': SEXES.MALE}


class NonUserEncounters(AllEncounters):
    title = u'Z toho osob blízkých'
    filtering = {'client_is_drug_user': False}


class IvEncounters(AllEncounters):
    title = u'z toho IV uživatelů'
    filtering = {'client_iv': True}


class NonClients(AggregationRow):
    title = u'Počet neuživatelů'
    aggregation_dbcol = 'person'
    excludes = {'person_model': 'client'}
    model = SearchEncounter


class Practitioners(AggregationRow):
    title = u'Počet neuživatelů'
    model = SearchEncounter
    aggregation_dbcol = 'person'
    filtering = {'person_model': 'practitioner'}


class AllAddresses(SumAggregationRow):
    title = u'Počet oslovených'
    aggregation_dbcol = 'nr_of_addresses'
    model = SearchEncounter


class NonDrugUserAddresses(AllAddresses):
    title = 'Z toho neUD'
    filtering = {'client_is_drug_user': False}


class IncomeExaminations(SumAggregationRow):
    title = u'Počet prvních kontaktů'
    model = SearchEncounter
    aggregation_dbcol = 'nr_of_incomeexaminations'


class MonthlyStats(Report):
    title = u'Měsíční statistiky'
    grouping = ('month', 'town')
    row_classes = (AllEncounters, MaleEncounters, NonUserEncounters,
        IvEncounters, NonClients, Practitioners, AllAddresses, NonDrugUserAddresses,
        IncomeExaminations)

    def _column_keys(self):
        return (hashdict((('month', month), ('town', town.pk)),) for town in Town.objects.all()
            for month in xrange(1, 13))
    column_keys = property(_column_keys)

    def column_title(self, key):
        return u'%s/%s' % (key['month'], key['town'])

    def __init__(self, year, *args, **kwargs):
        self.additional_filtering = {'year': year}
        super(MonthlyStats, self).__init__(*args, **kwargs)
