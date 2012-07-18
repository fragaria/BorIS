from datetime import date
from copy import copy

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from nose import tools

from boris.classification import SEXES, DRUG_APPLICATION_TYPES, \
        ANONYMOUS_TYPES, DISEASES
from boris.clients.models import Anonymous
from boris.syringes.models import SyringeCollection
from boris.services.models.core import Encounter
from boris.services.models.basic import Address, PhoneCounseling, \
        HarmReduction, IncomeExamination, DiseaseTest
from boris.reporting.reports.monthly_stats import AllClientEncounters, \
        MaleClientEncounters, IvClientEncounters, NonUserClientEncounters, \
        NonClients, Parents, Practitioners, AllAddresses, AddressesDU, \
        EncounterCount, ClientEncounterCount, \
        PractitionerEncounterCount, PhoneEncounterCount, FirstContactCount, \
        FirstContactCountDU, FirstContactCountIV, HarmReductionCount, \
        GatheredSyringes, IssuedSyringes, SyringeCollectionCount, disease_tests
from boris.reporting.core import make_key
from boris.reporting.management import install_views

from test_boris.helpers import get_tst_town, get_tst_client, \
        get_tst_drug, get_tst_practitioner

def create_encounter(person, date, town=None):
    if not town:
        town = person.town

    return Encounter.objects.create(person=person, performed_on=date, where=town)

def create_service(service_class, person, date, town, kwargs_dict={}):
    e = Encounter.objects.create(person=person, performed_on=date, where=town)
    service_kwargs = copy(kwargs_dict)
    service_kwargs.update({
        'encounter': e,
        'content_type': ContentType.objects.get_by_natural_key('services',
            service_class.__name__),
    })

    return service_class.objects.create(**service_kwargs)

def create_syringe_collection(town, date, count):
    return SyringeCollection.objects.create(date=date, town=town, count=count,
            location='')


class MockMonthlyReport(object):
    grouping = ('month', 'town')
    grouping_total = ('month',)
    additional_filtering = {'year': 2011}

class MockYearlyReport(object):
    grouping = ('month',)
    grouping_total = ('year',)
    additional_filtering = {'year': 2011}

class TestEncounterAggregations(TestCase):
    """ Mostly encounter aggregations are tested here. """

    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()
        self.drug = get_tst_drug()

        # clients
        self.client1 = get_tst_client('c1', {'town': self.town1, 'primary_drug': self.drug})
        self.client2 = get_tst_client('c2', {'town': self.town1, 'primary_drug': self.drug, 'primary_drug_usage': DRUG_APPLICATION_TYPES.VEIN_INJECTION})
        self.client3 = get_tst_client('c3', {'town': self.town1, 'sex': SEXES.FEMALE, 'close_person': True})
        self.client4 = get_tst_client('c4', {'town': self.town1})
        self.client5 = get_tst_client('c5', {'town': self.town2})
        self.client6 = get_tst_client('c6', {'town': self.town2})
        self.client7 = get_tst_client('c7', {'town': self.town2})

        create_encounter(self.client1, date(2011, 11, 1))
        create_encounter(self.client1, date(2011, 11, 1))
        create_encounter(self.client1, date(2011, 12, 1))
        create_encounter(self.client2, date(2011, 11, 1))
        create_encounter(self.client3, date(2011, 11, 1))
        create_encounter(self.client3, date(2011, 11, 1))
        create_encounter(self.client4, date(2011, 12, 1))
        create_encounter(self.client5, date(2011, 11, 1))
        create_encounter(self.client5, date(2011, 11, 1))
        create_encounter(self.client5, date(2011, 11, 1))
        create_encounter(self.client6, date(2010, 11, 1))
        create_encounter(self.client6, date(2011, 7, 1))
        create_encounter(self.client6, date(2011, 11, 1))

        # anonymous
        self.anonym1 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.IV)
        self.anonym2 = Anonymous.objects.get(sex=SEXES.FEMALE,
                drug_user_type=ANONYMOUS_TYPES.IV)
        self.anonym3 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.NON_USER_PARENT)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym2, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym3, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym2, date(2011, 12, 1), self.town1)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town2)

        # practitioners
        self.practitioner1 = get_tst_practitioner('sroubek1')
        self.practitioner2 = get_tst_practitioner('sroubek2')
        create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
        create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
        create_encounter(self.practitioner2, date(2011, 11, 1), self.town1)
        create_encounter(self.practitioner2, date(2011, 12, 1), self.town1)

        self.report = MockMonthlyReport()

    def test_all_client_encounters(self):
        aggregation = AllClientEncounters(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 3)

    def test_male_client_encounters(self):
        aggregation = MaleClientEncounters(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_iv_client_encounters(self):
        aggregation = IvClientEncounters(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 1)

    def test_nonuser_client_encounters(self):
        aggregation = NonUserClientEncounters(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 1)

    def test_nonclient_encounters(self):
        aggregation = NonClients(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 6)

    def test_parents(self):
        aggregation = Parents(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 1)

    def test_practitioners(self):
        aggregation = Practitioners(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 2)


class TestServiceAggregations(TestCase):
    """ Mostly service aggregations are tested here. """

    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()
        self.drug = get_tst_drug()

        # persons
        self.client1 = get_tst_client('c1', {'town': self.town1, 'primary_drug': self.drug})
        self.client2 = get_tst_client('c2', {'town': self.town2, 'primary_drug': self.drug})
        self.client3 = get_tst_client('c3', {'town': self.town1})
        self.anonym1 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.IV)
        self.anonym2 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.NON_USER)
        self.practitioner1 = get_tst_practitioner('sroubek')

        # services - addresses
        create_service(Address, self.client1, date(2011, 11, 1), self.town1)
        create_service(Address, self.client1, date(2011, 11, 1), self.town2)
        create_service(Address, self.client1, date(2011, 12, 1), self.town2)
        create_service(Address, self.client3, date(2011, 11, 1), self.town1)
        create_service(Address, self.anonym1, date(2011, 11, 1), self.town1)
        create_service(Address, self.anonym1, date(2011, 11, 1), self.town1)
        create_service(Address, self.anonym2, date(2011, 11, 1), self.town1)

        # services - income examinations
        create_service(IncomeExamination, self.client1, date(2011, 11, 1), self.town1)
        create_service(IncomeExamination, self.client3, date(2011, 11, 1), self.town1)
        create_service(IncomeExamination, self.client2, date(2011, 12, 1), self.town1)

        # services - harm reduction
        hr_kwargs = {
            'in_count': 5,
            'out_count': 10,
        }
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client2, date(2011, 11, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client2, date(2011, 11, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client1, date(2011, 12, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town2, hr_kwargs)

        # services - disease tests
        create_service(DiseaseTest, self.client1, date(2011, 11, 1), self.town1, {'disease': DISEASES.VHC})
        create_service(DiseaseTest, self.client1, date(2011, 12, 1), self.town1, {'disease': DISEASES.VHC})
        create_service(DiseaseTest, self.client1, date(2011, 11, 1), self.town2, {'disease': DISEASES.VHC})
        create_service(DiseaseTest, self.client1, date(2011, 11, 1), self.town2, {'disease': DISEASES.HIV})

        self.report = MockMonthlyReport()

    def test_all_addresses(self):
        aggregation = AllAddresses(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 5)

    def test_all_addresses_du(self):
        aggregation = AddressesDU(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 3)

    def test_first_contact_count(self):
        aggregation = FirstContactCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 5)

    def test_first_contact_count_du(self):
        aggregation = FirstContactCountDU(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 3)

    def test_first_contact_count_iv(self):
        aggregation = FirstContactCountIV(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_harm_reduction_count(self):
        aggregation = HarmReductionCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 3)

    def test_gathered_syringes(self):
        aggregation = GatheredSyringes(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 15)

    def test_issued_syringes(self):
        aggregation = IssuedSyringes(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 30)

    def test_disease_vhc(self):
        tools.assert_true('DiseaseTestVHC' in (dtest.__name__ for dtest in disease_tests))
        for disease_test in disease_tests:
            if disease_test.__name__ == 'DiseaseTestVHC':
                aggregation = disease_test(self.report)
                break
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 1)


class TestMixedAggregations(TestCase):
    """
    In these aggregations, both encounters and services are taken into account.
    """

    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()

        # persons
        self.client1 = get_tst_client('c1', {'town': self.town1})
        self.client2 = get_tst_client('c2', {'town': self.town1})
        self.anonym = Anonymous.objects.get(sex=SEXES.MALE,
            drug_user_type=ANONYMOUS_TYPES.IV)
        self.practitioner = get_tst_practitioner('sroubek1')

        # services
        create_service(Address, self.client1, date(2011, 11, 1), self.town1)
        create_service(Address, self.client2, date(2011, 11, 1), self.town1)
        create_service(Address, self.client1, date(2011, 12, 1), self.town1)
        create_service(Address, self.client1, date(2011, 11, 1), self.town2)
        create_service(Address, self.anonym, date(2011, 11, 1), self.town1)
        create_service(Address, self.practitioner, date(2011, 11, 1), self.town1)
        create_service(Address, self.practitioner, date(2011, 11, 1), self.town2)
        create_service(PhoneCounseling, self.practitioner, date(2011, 11, 1), self.town1)
        create_service(PhoneCounseling, self.client1, date(2011, 11, 1), self.town1)
        create_service(PhoneCounseling, self.anonym, date(2011, 11, 1), self.town1)

        self.report = MockMonthlyReport()

    def test_encounter_count(self):
        aggregation = EncounterCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 7)

    def test_client_encounter_count(self):
        aggregation = ClientEncounterCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_practitioner_encounter_count(self):
        aggregation = PractitionerEncounterCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_phone_encounter_count(self):
        aggregation = PhoneEncounterCount(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 3)


class TestEncounterTotals(TestCase):

    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()

        # clients
        self.client1 = get_tst_client('c1', {'town': self.town1, })
        self.client2 = get_tst_client('c2', {'town': self.town1, })

        create_encounter(self.client1, date(2011, 11, 1))
        create_encounter(self.client1, date(2011, 11, 1), self.town2)
        create_encounter(self.client1, date(2011, 11, 1))
        create_encounter(self.client2, date(2011, 11, 1), self.town2)
        create_encounter(self.client2, date(2011, 12, 1), self.town2)

        # anonymous
        self.anonym1 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.IV)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
        create_encounter(self.anonym1, date(2011, 11, 1), self.town2)

        # practitioners
        self.practitioner1 = get_tst_practitioner('sroubek1')
        self.practitioner2 = get_tst_practitioner('sroubek2')
        create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
        create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
        create_encounter(self.practitioner2, date(2011, 11, 1), self.town2)
        create_encounter(self.practitioner2, date(2011, 12, 1), self.town1)

        self.monthly_report = MockMonthlyReport()
        self.yearly_report = MockYearlyReport()

    def test_all_client_encounters_total_monthly(self):
        aggregation = AllClientEncounters(self.monthly_report)
        key = make_key({'month': 11})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_all_client_encounters_total_yearly(self):
        aggregation = AllClientEncounters(self.yearly_report)
        key = make_key({'year': 2011})
        tools.assert_equals(aggregation.get_val(key), 2)

    def test_nonclient_encounters_monthly(self):
        aggregation = NonClients(self.monthly_report)
        key = make_key({'month': 11})
        tools.assert_equals(aggregation.get_val(key), 5)

    def test_nonclient_encounters_yearly(self):
        aggregation = NonClients(self.yearly_report)
        key = make_key({'year': 2011})
        tools.assert_equals(aggregation.get_val(key), 5)


class TestServiceTotals(TestCase):

    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()

        # clients
        self.client1 = get_tst_client('c1', {'town': self.town1, })
        self.client2 = get_tst_client('c2', {'town': self.town1, })

        hr_kwargs = {
            'in_count': 5,
            'out_count': 17,
        }
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town1, hr_kwargs)
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town2, hr_kwargs)
        create_service(HarmReduction, self.client1, date(2011, 12, 1), self.town1, hr_kwargs)

        self.monthly_report = MockMonthlyReport()
        self.yearly_report = MockYearlyReport()

    def test_gathered_syringes_monthly(self):
        aggregation = GatheredSyringes(self.monthly_report)
        key = make_key({'month': 11})
        tools.assert_equals(aggregation.get_val(key), 15)

    def test_gathered_syringes_yearly(self):
        aggregation = GatheredSyringes(self.yearly_report)
        key = make_key({'year': 2011})
        tools.assert_equals(aggregation.get_val(key), 20)


class TestSyringeCollection(TestCase):
    def setUp(self):
        install_views('')
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()

        create_syringe_collection(self.town1, date(2011, 11, 1), 10)
        create_syringe_collection(self.town1, date(2011, 11, 1), 10)
        create_syringe_collection(self.town1, date(2011, 11, 1), 10)
        create_syringe_collection(self.town1, date(2011, 12, 1), 17)
        create_syringe_collection(self.town2, date(2011, 11, 1), 10)

        self.monthly_report = MockMonthlyReport()

    def test_syringe_collection(self):
        aggregation = SyringeCollectionCount(self.monthly_report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        tools.assert_equals(aggregation.get_val(key), 30)
