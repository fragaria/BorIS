# -*- encoding: utf8 -*-

from datetime import date

from boris.reporting.reports.clients import ClientReport
from boris.tests.helpers import (get_tst_client, InitialDataTestCase)

FAKE_TODAY = date(2017, 12, 12)


class TestClientAvgAge(InitialDataTestCase):
    def setUp(self):
        self.client1 = get_tst_client('aaa', {'birthdate': date(2000, 11, 20)})
        self.client2 = get_tst_client('bbb', {'birthdate': date(2010, 11, 1)})
        self.client3 = get_tst_client('ccc', {'birthdate': None})
        self.client4 = get_tst_client('ddd', {'birthdate_year_only': 1, 'birthdate': date(1993, 1, 1)})
        self.client5 = get_tst_client('eee', {'birthdate': date(2016, 12, 1)})

    def test_avg_age_normal_client_with_birthday(self):
        avg = ClientReport.get_average_age([self.client1, self.client2], FAKE_TODAY)
        self.assertEqual(avg, 12)

    def test_avg_with_none(self):
        avg = ClientReport.get_average_age([self.client1, self.client3], FAKE_TODAY)
        self.assertEqual(avg, 17)

    def test_avg_age_with_birthdate_year_only(self):
        avg = ClientReport.get_average_age([self.client1, self.client2, self.client4], FAKE_TODAY)
        self.assertEqual(avg, 16)

    def test_avg_age_with_birthdate_infant(self):
        avg = ClientReport.get_average_age([self.client5], FAKE_TODAY)
        self.assertEqual(avg, 1)

    def test_avg_age_with_all_type_of_client(self):
        avg = ClientReport.get_average_age([self.client1, self.client2, self.client3, self.client4], FAKE_TODAY)
        self.assertEqual(avg, 16)

    def test_date(self):
        avg = ClientReport.get_average_age([self.client1, self.client2, self.client3, self.client4], date(2016, 12, 12))
        self.assertEqual(avg, 15)