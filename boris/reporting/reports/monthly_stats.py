# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from boris.classification import SEXES
from boris.clients.models import Town
from boris.reporting.core import AggregationRow, QuerySetReport,\
    SumAggregationRow
from boris.reporting.models import SearchEncounter

class PersonBasedRow(AggregationRow):
    aggregation_dbcol = 'person'


class AllEncounters(PersonBasedRow):
    title = u'Počet klientů'


class MaleEncounters(PersonBasedRow):
    title = u'Z toho mužů' 
    additional_filtering = {'client_sex': SEXES.MALE}
    
    
class NonUserEncounters(PersonBasedRow):
    title = u'Z toho osob blízkých'
    additional_filtering = {'client_is_drug_user': False}
    
    
class IvEncounters(PersonBasedRow):
    title = u'z toho IV uživatelů'
    additional_filtering = {'client_iv': True}
    
    
class NonClients(PersonBasedRow):
    title = u'Počet neuživatelů'
    additional_excludes = {'person_model': 'client'}
    
    
class Practitioners(PersonBasedRow):
    title = u'Počet neuživatelů'
    additional_filtering = {'person_model': 'practitioner'}
    
    
class Addresses(SumAggregationRow):
    title = u'Počet oslovených'
    aggregation_dbcol = 'nr_of_addresses' 
    

class NonDrugUserAddresses(Addresses):
    title = 'Z toho neUD'
    additional_filtering = {'client_is_drug_user': False}
    
    
class IncomeExaminations(SumAggregationRow):
    title = u'Počet prvních kontaktů'
    aggregation_dbcol = 'nr_of_incomeexaminations'
    
    
class MonthlyStats(QuerySetReport):
    title = u'Měsíční statistiky'
    grouping = ('month', 'town')
    row_classes = (AllEncounters, MaleEncounters, NonUserEncounters,
        IvEncounters, NonClients, Practitioners, Addresses, NonDrugUserAddresses,
        IncomeExaminations)
    
    def _column_keys(self):
        return ({'month': month, 'town': town.pk} for town in Town.objects.all()
            for month in xrange(1, 13))
    column_keys = property(_column_keys)
    
    def column_title(self, key):
        return u'%s/%s' % (key['month'], key['town'])
    
    def get_base_qset(self):
        return SearchEncounter.objects.filter(year=self.year)
    
    def __init__(self, year, *args, **kwargs):
        self.year = year
        super(MonthlyStats, self).__init__(*args, **kwargs)
            
            