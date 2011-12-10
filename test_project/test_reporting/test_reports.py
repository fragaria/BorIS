from datetime import date
from djangosanetesting.cases import DatabaseTestCase

from boris.classification import SEXES, PRIMARY_DRUG_APPLICATION_TYPES
from boris.clients.models import Client, Town, Anonymous
from boris.services.models.core import Encounter
from boris.reporting.reports.monthly_stats import AllClientEncounters,\
        MaleClientEncounters, IvClientEncounters, NonUserClientEncounters, NonClients
from boris.reporting.core import make_key
from boris.reporting.management import install_views

from test_project.helpers import get_testing_town, get_testing_client, get_testing_drug

def create_encounter(person, date, town=None):
    if not town:
        town = person.town
    Encounter.objects.create(person=person, performed_on=date, where=town)

class MockMonthlyReport(object):
    grouping = ('month', 'town')
    additional_filtering = {'year': 2011}

class TestAggregations(DatabaseTestCase):

  def setUp(self):
      install_views(None, None, 1) # TODO: find out why this is not done automatically
      self.town1 = get_testing_town()
      self.town2 = get_testing_town()
      self.drug = get_testing_drug()

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

      self.anonym1 = Anonymous.objects.all()[0]
      self.anonym2 = Anonymous.objects.all()[1]
      create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
      create_encounter(self.anonym2, date(2011, 11, 1), self.town1)
      create_encounter(self.anonym1, date(2011, 11, 1), self.town1)
      create_encounter(self.anonym2, date(2011, 12, 1), self.town1)
      create_encounter(self.anonym1, date(2011, 11, 1), self.town2)

      self.report = MockMonthlyReport()


  def tearDown(self): # TODO: why is this necessary? (NOTE: it is still faster than DestructiveDatabaseTestCase)
      Client.objects.all().delete()
      Town.objects.all().delete()
      Encounter.objects.all().delete()

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
      self.assert_equals(aggregation.get_val(key), 2)
