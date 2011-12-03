# -*- encoding: utf-8 -*-
'''
Created on 27.11.2011

@author: xaralis
'''
from django.db.models import Q

from boris.classification import SEXES, PRIMARY_DRUG_APPLICATION_TYPES, ANONYMOUS_TYPES,\
    DISEASES
from boris.clients.models import Town
from boris.reporting.core import Aggregation, Report,\
    SumAggregation, make_key
from boris.reporting.models import SearchEncounter, SearchService

class EncounterAggregation(Aggregation): model = SearchEncounter
class ServiceAggregation(Aggregation):   model = SearchService


class AllClientEncounters(EncounterAggregation):
    title = u'Počet klientů'
    aggregation_dbcol = 'person'
    filtering = {'is_client': True}


class IvClientEncounters(AllClientEncounters):
    title = u'z toho injekčních uživatelů drog'
    filtering = {'is_client': True, 'primary_drug_usage': PRIMARY_DRUG_APPLICATION_TYPES.IV}


class MaleClientEncounters(AllClientEncounters):
    title = u'Z toho mužů'
    filtering = {'is_client': True, 'client_sex': SEXES.MALE}


class NonUserClientEncounters(AllClientEncounters):
    title = u'Z toho osob blízkých (sex. partneři)'
    filtering = {'is_client': True, 'primary_drug__isnull': True}


class NonClients(EncounterAggregation):
    title = u'Počet neuživatelů, kteří využili alespoň jednou služeb programu'
    aggregation_dbcol = 'person'
    excludes = {'is_client': False}
    

class Parents(NonClients):
    title = u'Z toho rodiče'
    filtering = {
        'person__anonymous__drug_user_type': ANONYMOUS_TYPES.NON_USER_PARENT,
        'is_anonymous': True
    }


class Practitioners(NonClients):
    title = u'Z toho odborná veřejnost'
    filtering = {'is_practitioner': True}


class AllAddresses(ServiceAggregation):
    title = u'Počet oslovených'
    aggregation_dbcol = 'id'
    filtering = {'content_type_model': 'address'}


class AddressesDU(AllAddresses):
    title = u'Z toho UD'
    filtering = {
        'content_type_model': 'address',
        'person__client__primary_drug__isnull': False
    }


class AddressesNonDU(AllAddresses):
    title = 'Z toho neUD'
    filtering = {
        'content_type_model': 'address',
        'person__client__primary_drug__isnull': True
    }


class DiseaseTestBase(ServiceAggregation):
    title = u'Počet testů VHC'
    filtering = {
        'content_type_model': 'diseasetest',
        'service__diseasetest__disease': DISEASES.VHC 
    }

disease_tests = []

for key, title in DISEASES:
    attrs = {
        'title': u'Počet testů %s' % title,
        'filtering': {
            'content_type_model': 'diseasetest',
            'service__diseasetest__disease': key
        }
    }
    DiseaseTestClass = type(str('DiseaseTest%s' % title), (DiseaseTestBase,), attrs)
    disease_tests.append(DiseaseTestClass)
    
    
class EncounterCount(EncounterAggregation):
    title = u'Počet kontaktů celkem'
    
    
class ClientEncounterCount(ServiceAggregation):
    title = u'z toho s klienty, uživateli drog, přímý'
    aggregation_dbcol = 'encounter'
    filtering = {'person__client__pk__isnull': False}
    excludes = {'content_type_model': 'phonecounseling'}
    
    
class PractitionerEncounterCount(EncounterCount):
    title = u'z toho s odbornou veřejností'
    filtering = {'is_practitioner': True}
    
    
class PhoneEncounterCount(EncounterCount):
    title = u'z toho telefonický kontakt'
    model = SearchService
    filtering = {'content_type_model': 'phonecounseling'}
    aggregation_dbcol = 'encounter'
    
    
class FirstContactCount(ServiceAggregation):
    title = u'Počet prvních kontaktů'
    filtering = Q(content_type_model='incomeexamination') | Q(content_type_model='address')
    

class FirstContactCountDU(FirstContactCount):
    title = u'z toho s UD'
    filtering = (
        Q(person__client__primary_drug__isnull=False) &
        Q(content_type_model='incomeexamination')
    ) | (
        Q(person__anonymous__drug_user_type__in=(ANONYMOUS_TYPES.IV, ANONYMOUS_TYPES.NON_IV)) &
        Q(content_type_model='address')
    )
    
    
class FirstContactCountIV(FirstContactCount):
    title = u'z toho nitrožilních UD'
    filtering = (
        Q(person__client__primary_drug__isnull=False) &
        Q(content_type_model='incomeexamination')
    ) | (
        Q(person__anonymous__drug_user_type=ANONYMOUS_TYPES.IV) &
        Q(content_type_model='address')
    )
    
    
class HarmReductionCount(ServiceAggregation):
    title = u'Počet výměn'
    filtering = {'content_type_model': 'harmreduction'}
    

class GatheredSyringes(SumAggregation, ServiceAggregation):
    title = u'Počet přijatého inj. materiálu'
    aggregation_dbcol = 'service__harmreduction__in_count'
    
    
class IssuedSyringes(SumAggregation, ServiceAggregation):
    title = u'Počet vydaného inj. materiálu'
    aggregation_dbcol = 'service__harmreduction__out_count'


class MonthlyStats(Report):
    title = u'Měsíční statistiky'
    grouping = ('month', 'town')
    aggregation_classes = [
        AllClientEncounters,
        MaleClientEncounters,
        NonUserClientEncounters,
        IvClientEncounters,
        NonClients,
        Practitioners,
        AllAddresses,
    ] + disease_tests + [
        EncounterCount,
        ClientEncounterCount,
        PractitionerEncounterCount,
        PhoneEncounterCount,
        FirstContactCount,
        FirstContactCountDU,
        FirstContactCountIV,
        HarmReductionCount,
        GatheredSyringes,
        IssuedSyringes
    ]
    
    def _columns(self):
        for town in Town.objects.all():
            yield town
    columns = property(_columns)

    def __init__(self, year, *args, **kwargs):
        self.year = year
        self.additional_filtering = {'year': year}
        super(MonthlyStats, self).__init__(*args, **kwargs)

    def get_data(self):
        data = [
            (month, [
                (aggregation.title, [
                    aggregation.get_val(
                        make_key((('month', month), ('town', town.pk)),)
                    ) for town in Town.objects.all()
                ]) for aggregation in self.aggregations
            ]) for month in xrange(1, 13)
        ]
        return data 
