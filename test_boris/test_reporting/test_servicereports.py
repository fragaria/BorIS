from datetime import date

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from boris.reporting.reports.services import ServiceReport
from boris.services.models import (Address, UtilityWork, SocialWork,
    InformationService, HarmReduction, service_list)
from test_boris.helpers import (get_tst_town, get_tst_client, get_tst_drug,
    create_service)


def remove_zero_stats(stats):
    for key, val in stats.items():
        if val == 0:
            del stats[key]

    return stats


class TestServiceReports(TestCase):

    def setUp(self):
        drug = get_tst_drug()
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()
        self.client1 = get_tst_client('c1', {'town': self.town1, 'primary_drug': drug})
        self.client2 = get_tst_client('c2', {'town': self.town1, 'primary_drug': drug})
        create_service(Address, self.client1, date(2011, 11, 1), self.town1)
        create_service(Address, self.client1, date(2011, 11, 3), self.town1)
        create_service(Address, self.client2, date(2011, 11, 1), self.town1)
        create_service(UtilityWork, self.client1, date(2011, 11, 1), self.town2)
        social_work_kwargs = {'other': True}
        create_service(SocialWork, self.client1, date(2012, 11, 1), self.town1, social_work_kwargs)
        create_service(SocialWork, self.client1, date(2011, 11, 1), self.town1)
        create_service(InformationService, self.client1, date(2011, 11, 1), self.town1)
        harm_reduction_kwargs = {'in_count': 87, 'condoms': True}
        create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town1, harm_reduction_kwargs)

    def test_no_filter(self):
        filtering = {}
        r = ServiceReport(**filtering)
        stats = remove_zero_stats(dict(r.get_stats()))
        expected = {
            Address.service.title: 3,
            UtilityWork.service.title: 1,
            SocialWork.service.title: 2,
            SocialWork._meta.get_field('other').verbose_name.__unicode__(): 1,
            InformationService.service.title: 1,
            HarmReduction.service.title: 1,
            HarmReduction._meta.get_field('condoms').verbose_name.__unicode__(): 1,
            HarmReduction._meta.get_field('in_count').verbose_name.__unicode__(): 87,
        }
        self.assertEqual(stats, expected)

    def test_filter_by_person(self):
        filtering = {'person': self.client2}
        r = ServiceReport(**filtering)
        stats = remove_zero_stats(dict(r.get_stats()))
        expected = {
            Address.service.title: 1
        }
        self.assertEqual(stats, expected)

    def test_filter_by_date_from(self):
        filtering = {'date_from': date(2012, 1, 1)}
        r = ServiceReport(**filtering)
        stats = remove_zero_stats(dict(r.get_stats()))
        expected = {
            SocialWork.service.title: 1,
            SocialWork._meta.get_field('other').verbose_name.__unicode__(): 1,
        }
        self.assertEqual(stats, expected)

    def test_filter_by_date_to(self):
        filtering = {'date_to': date(2010, 1, 1)}
        r = ServiceReport(**filtering)
        stats = remove_zero_stats(dict(r.get_stats()))
        expected = {}
        self.assertEqual(stats, expected)

    def test_filter_by_town(self):
        filtering = {'town': self.town2}
        r = ServiceReport(**filtering)
        stats = remove_zero_stats(dict(r.get_stats()))
        expected = {
            UtilityWork.service.title: 1
        }
        self.assertEqual(stats, expected)

    def test_include_in_reports(self):
        classes = [s for s in service_list() if s.service.include_in_reports]
        stats = dict(ServiceReport().get_stats())
        for c in classes:
            self.assertTrue(c.service.title in stats)
