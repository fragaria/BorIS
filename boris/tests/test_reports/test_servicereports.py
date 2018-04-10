# -*- encoding: utf8 -*-

from datetime import date
import sys

from django.core.handlers.wsgi import WSGIRequest
from django.core.servers.basehttp import ServerHandler
from django.http import Http404
from django.test import TestCase
from nose import tools

from boris.classification import DRUGS
from boris.reporting.reports.services import ServiceReport
from boris.services import views
from boris.services.models import (Approach, UtilityWork, SocialWork,
                                   InformationService, HarmReduction, service_list, Encounter)
from boris.services.views import HandleForm
from boris.tests.helpers import (get_tst_town, get_tst_client, create_service)


def normalize_stats(stats):
    stats = dict(stats)
    clean_stats = {}
    for service, services in stats.items():
        non_zero_services = []
        for title, count in services:
            if count != 0 and count != '-':
                non_zero_services.append((title, count))
        if non_zero_services:
            clean_stats[service] = tuple(non_zero_services)
    return clean_stats


class TestServiceReports(TestCase):

    maxDiff = None

    def setUp(self):
        drug = DRUGS.HEROIN
        self.town1 = get_tst_town()
        self.town2 = get_tst_town()
        self.client1 = get_tst_client('c1', {'town': self.town1, 'primary_drug': drug})
        self.client2 = get_tst_client('c2', {'town': self.town1, 'primary_drug': drug})
        create_service(Approach, self.client1, date(2011, 11, 1), self.town1)
        create_service(Approach, self.client1, date(2011, 11, 3), self.town1)
        create_service(Approach, self.client2, date(2011, 11, 1), self.town1)
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
        stats = normalize_stats(r._get_service_stats())
        expected = {
            Approach: ((Approach.service.title, 3),),
            UtilityWork: ((UtilityWork.service.title, 1),),
            SocialWork: ((SocialWork.service.title, 2), (SocialWork._meta.get_field('other').verbose_name.__unicode__(), 1)),
            # InformationService: ((InformationService.service.title, 1),),
            HarmReduction: ((HarmReduction.service.title, 1), (HarmReduction._meta.get_field('condoms').verbose_name.__unicode__(), 1), (HarmReduction._meta.get_field('in_count').verbose_name.__unicode__(), 87))
        }
        self.assertEqual(stats, expected)

    def test_filter_by_person(self):
        filtering = {'person': self.client2}
        r = ServiceReport(**filtering)
        stats = normalize_stats(r._get_service_stats())
        expected = {
            Approach: ((Approach.service.title, 1),)
        }
        self.assertEqual(stats, expected)

    def test_filter_by_date_from(self):
        filtering = {'date_from': date(2012, 1, 1)}
        r = ServiceReport(**filtering)
        stats = normalize_stats(r._get_service_stats())
        expected = {
            SocialWork: ((SocialWork.service.title, 1), (SocialWork._meta.get_field('other').verbose_name.__unicode__(), 1))
        }
        self.assertEqual(stats, expected)

    def test_filter_by_date_to(self):
        filtering = {'date_to': date(2010, 1, 1)}
        r = ServiceReport(**filtering)
        stats = normalize_stats(r.get_stats())
        expected = {None: ((u'Počet kontaktů (z toho přímých)', '0 (0)'), )}
        self.assertEqual(stats, expected)

    def test_filter_by_town(self):
        filtering = {'towns': [self.town2]}
        r = ServiceReport(**filtering)
        stats = normalize_stats(r._get_service_stats())
        expected = {
            UtilityWork: ((UtilityWork.service.title, 1),)
        }
        self.assertEqual(stats, expected)

    def test_include_in_reports(self):
        classes = [s for s in service_list() if s.service.include_in_reports]
        stat_classes = [s[0] for s in ServiceReport()._get_service_stats()]
        self.assertEqual(sorted(classes), sorted(stat_classes))

    def test_encounter_first(self):
        e1 = Encounter.objects.first(2011)
        e2 = Encounter.objects.first(2011, [self.town1])

        self.assertEqual(len(e1), 6)
        self.assertEqual(len(e2), 5)
        self.assertEqual(e1[0].service_count(), 1)


class TestServices(TestCase):
    def setUp(self):
        drug = DRUGS.HEROIN
        self.town1 = get_tst_town()
        self.client1 = get_tst_client('c1', {'town': self.town1, 'primary_drug': drug})
        self.harm_reduction = create_service(HarmReduction, self.client1, date(2011, 11, 1), self.town1)
        self.encounter = Encounter.objects.filter(person=self.client1)[0]
        handler = ServerHandler(sys.stdin, sys.stdout, sys.stderr, {'REQUEST_METHOD': 'POST'})
        handler.setup_environ()
        self.request = WSGIRequest(handler.environ)

    def test_context(self):
        ctx = HandleForm().get_context(self.request, self.encounter.id, 'HarmReduction', self.harm_reduction.id)
        # render = HandleForm().__call__(self.request, self.encounter.id, 'HarmReduction', 1)
        #
        # self.assertEqual(render.status_code, 200)
        self.assertEqual(ctx['encounter'], self.encounter)
        # self.assertFalse(ctx['is_edit'])
        self.assertEqual(ctx['service'], HarmReduction)

    def test_services_list(self):
        services_list = views.services_list(self.request, self.encounter.id)
        self.assertEqual(services_list.status_code, 200)

    @tools.raises(Http404)
    def test_drop_service(self):
        views.drop_service(self.request, -1)
