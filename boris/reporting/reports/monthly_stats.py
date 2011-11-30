# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from boris.classification import SEXES
from boris.clients.models import Town
from boris.reporting.core import AggregationRow, QuerySetReport,\
    SumAggregationRow, hashdict
from boris.reporting.models import SearchEncounter

class PersonBasedRow(AggregationRow):
    aggregation_dbcol = 'person'


class AllEncounters(PersonBasedRow):
    title = u'Počet klientů'
    model = SearchEncounter


class MaleEncounters(PersonBasedRow):
    title = u'Z toho mužů'
    filtering = {'client_sex': SEXES.MALE}
    model = SearchEncounter


class NonUserEncounters(PersonBasedRow):
    title = u'Z toho osob blízkých'
    filtering = {'client_is_drug_user': False}
    model = SearchEncounter


class IvEncounters(PersonBasedRow):
    title = u'z toho IV uživatelů'
    filtering = {'client_iv': True}
    model = SearchEncounter


class NonClients(PersonBasedRow):
    title = u'Počet neuživatelů'
    excludes = {'person_model': 'client'}
    model = SearchEncounter


class Practitioners(PersonBasedRow):
    title = u'Počet neuživatelů'
    filtering = {'person_model': 'practitioner'}
    model = SearchEncounter


class Addresses(SumAggregationRow):
    title = u'Počet oslovených'
    aggregation_dbcol = 'nr_of_addresses'
    model = SearchEncounter


class NonDrugUserAddresses(Addresses):
    title = 'Z toho neUD'
    filtering = {'client_is_drug_user': False}


class IncomeExaminations(SumAggregationRow):
    title = u'Počet prvních kontaktů'
    aggregation_dbcol = 'nr_of_incomeexaminations'
    model = SearchEncounter


class MonthlyStats(QuerySetReport):
    title = u'Měsíční statistiky'
    grouping = ('month', 'town')
    row_classes = (AllEncounters, MaleEncounters, NonUserEncounters,
        IvEncounters, NonClients, Practitioners, Addresses, NonDrugUserAddresses,
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
