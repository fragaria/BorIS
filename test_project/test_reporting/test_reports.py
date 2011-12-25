from datetime import date
from djangosanetesting.cases import DatabaseTestCase
from copy import copy

from django.contrib.contenttypes.models import ContentType

from boris.classification import SEXES, PRIMARY_DRUG_APPLICATION_TYPES, ANONYMOUS_TYPES
from boris.clients.models import Client, Town, Anonymous, Practitioner
from boris.services.models.core import Encounter, Service
from boris.reporting.reports.monthly_stats import AllClientEncounters,\
        MaleClientEncounters, IvClientEncounters, NonUserClientEncounters,\
        NonClients, Parents, Practitioners, AllAddresses, AddressesDU,\
        AddressesNonDU
from boris.reporting.core import make_key
from boris.reporting.management import install_views

from test_project.helpers import get_testing_town, get_testing_client,\
        get_testing_drug, get_testing_practitioner

def create_encounter(person, date, town=None):
    if not town:
        town = person.town

    return Encounter.objects.create(person=person, performed_on=date, where=town)

def create_service(service_class_name, person, date, town, kwargs_dict={}):
    e = Encounter.objects.create(person=person, performed_on=date, where=town)
    service_kwargs = copy(kwargs_dict)
    service_kwargs.update({
        'encounter': e,
        'content_type': ContentType.objects.get_by_natural_key('services',
            service_class_name),
    })

    return Service.objects.create(**service_kwargs)


class MockMonthlyReport(object):
    grouping = ('month', 'town')
    additional_filtering = {'year': 2011}

class TestEncounterAggregations(DatabaseTestCase):

  def setUp(self):
      install_views(None, None, 1) # TODO: find out why this is not done automatically
      self.town1 = get_testing_town()
      self.town2 = get_testing_town()
      self.drug = get_testing_drug()

      # clients
      self.client1 = get_testing_client('c1', {'town': self.town1, 'primary_drug': self.drug})
      self.client2 = get_testing_client('c2', {'town': self.town1, 'primary_drug': self.drug, 'primary_drug_usage': PRIMARY_DRUG_APPLICATION_TYPES.IV})
      self.client3 = get_testing_client('c3', {'town': self.town1, 'sex': SEXES.FEMALE})
      self.client4 = get_testing_client('c4', {'town': self.town1})
      self.client5 = get_testing_client('c5', {'town': self.town2})
      self.client6 = get_testing_client('c6', {'town': self.town2})
      self.client7 = get_testing_client('c7', {'town': self.town2})

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
      self.practitioner1 = get_testing_practitioner('sroubek1')
      self.practitioner2 = get_testing_practitioner('sroubek2')
      create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
      create_encounter(self.practitioner1, date(2011, 11, 1), self.town1)
      create_encounter(self.practitioner2, date(2011, 11, 1), self.town1)
      create_encounter(self.practitioner2, date(2011, 12, 1), self.town1)

      # services

      self.report = MockMonthlyReport()


  def tearDown(self): # TODO: why is this necessary? (NOTE: it is still faster than DestructiveDatabaseTestCase)
      Client.objects.all().delete()
      Town.objects.all().delete()
      Encounter.objects.all().delete()
      Practitioner.objects.all().delete()
      Service.objects.all().delete()

  def test_all_client_encounters(self):
      aggregation = AllClientEncounters(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 3)

  def test_male_client_encounters(self):
      aggregation = MaleClientEncounters(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 2)

  def test_iv_client_encounters(self):
      aggregation = IvClientEncounters(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 1)

  def test_nonuser_client_encounters(self):
      aggregation = NonUserClientEncounters(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 1)

  def test_nonclient_encounters(self):
      aggregation = NonClients(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 6)

  def test_parents(self):
      aggregation = Parents(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 1)

  def test_practitioners(self):
      aggregation = Practitioners(self.report)
      key = make_key({'month': 11, 'town': self.town1.pk})
      self.assert_equals(aggregation.get_val(key), 2)


class TestServiceAggregations(DatabaseTestCase):
    def setUp(self):
        install_views(None, None, 1) # TODO: find out why this is not done automatically
        self.town1 = get_testing_town()
        self.town2 = get_testing_town()
        self.drug = get_testing_drug()

        # persons
        self.client1 = get_testing_client('c1', {'town': self.town1, 'primary_drug': self.drug})
        self.client2 = get_testing_client('c2', {'town': self.town2, 'primary_drug': self.drug})
        self.client3 = get_testing_client('c3', {'town': self.town1})
        self.anonym1 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.IV)
        self.anonym2 = Anonymous.objects.get(sex=SEXES.MALE,
                drug_user_type=ANONYMOUS_TYPES.NON_USER)
        self.practitioner1 = get_testing_practitioner('sroubek')

        # services - addresses
        create_service('Address', self.client1, date(2011, 11, 1), self.town1)
        create_service('Address', self.client1, date(2011, 11, 1), self.town2)
        create_service('Address', self.client1, date(2011, 12, 1), self.town2)
        create_service('Address', self.client3, date(2011, 11, 1), self.town1)
        create_service('Address', self.anonym1, date(2011, 11, 1), self.town1)
        create_service('Address', self.anonym1, date(2011, 11, 1), self.town1)
        create_service('Address', self.anonym2, date(2011, 11, 1), self.town1)

        self.report = MockMonthlyReport()

    def tearDown(self):
        Client.objects.all().delete()
        Town.objects.all().delete()
        Encounter.objects.all().delete()
        Practitioner.objects.all().delete()
        Service.objects.all().delete()

    def test_all_addresses(self):
        aggregation = AllAddresses(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        self.assert_equals(aggregation.get_val(key), 5)

    def test_all_addresses_du(self):
        aggregation = AddressesDU(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        self.assert_equals(aggregation.get_val(key), 3)

    def test_all_addresses_non_du(self):
        aggregation = AddressesNonDU(self.report)
        key = make_key({'month': 11, 'town': self.town1.pk})
        self.assert_equals(aggregation.get_val(key), 2)

