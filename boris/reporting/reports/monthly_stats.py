# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from boris.classification import SEXES, PRIMARY_DRUG_APPLICATION_TYPES
from boris.clients.models import Town
from boris.reporting.core import Aggregation, Report,\
    SumAggregation, hashdict
from boris.reporting.models import SearchEncounter, SearchService

class AllClientEncounters(Aggregation):
    title = u'Počet klientů'
    model = SearchEncounter
    aggregation_dbcol = 'person'
    filtering = {'is_client': True}


class MaleClientEncounters(AllClientEncounters):
    title = u'Z toho mužů'
    filtering = {'is_client': True, 'client_sex': SEXES.MALE}


class NonUserClientEncounters(AllClientEncounters):
    title = u'Z toho osob blízkých'
    filtering = {'is_client': True, 'primary_drug__isnull': True}


class IvClientEncounters(AllClientEncounters):
    title = u'z toho IV uživatelů'
    filtering = {'is_client': True, 'primary_drug_usage': PRIMARY_DRUG_APPLICATION_TYPES.IV}


class NonClients(Aggregation):
    title = u'Počet neuživatelů'
    aggregation_dbcol = 'person'
    excludes = {'is_client': False}
    model = SearchEncounter


class Practitioners(Aggregation):
    title = u'Počet neuživatelů'
    model = SearchEncounter
    aggregation_dbcol = 'person'
    filtering = {'is_practitioner': True}


class AllAddresses(Aggregation):
    title = u'Počet oslovených'
    model = SearchService
    aggregation_dbcol = 'id'
    filtering = {'content_type_model': 'address'}


#class NonDrugUserAddresses(AllAddresses):
#    title = 'Z toho neUD'
#    filtering = {'client_is_drug_user': False}


class IncomeExaminations(Aggregation):
    title = u'Počet prvních kontaktů'
    model = SearchService
    aggregation_dbcol = 'id'
    filtering = {'content_type_model': 'incomeexamination'}


class MonthlyStats(Report):
    title = u'Měsíční statistiky'
    grouping = ('month', 'town')
    columns = [town for town in Town.objects.all()]
    aggregation_classes = (AllClientEncounters, MaleClientEncounters, NonUserClientEncounters,
        IvClientEncounters, NonClients, Practitioners, AllAddresses, IncomeExaminations)

    def __init__(self, year, *args, **kwargs):
        self.year = year
        self.additional_filtering = {'year': year}
        super(MonthlyStats, self).__init__(*args, **kwargs)

    def get_data(self):
        return [
            (month, [
                (aggregation.title, [
                    aggregation.get_val(
                        hashdict((('month', month), ('town', town.pk)),)
                    ) for town in Town.objects.all()
                ]) for aggregation in self.aggregations
            ]) for month in xrange(1, 13)
        ]
