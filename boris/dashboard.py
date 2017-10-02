# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import ModelList, DashboardModule
from boris import settings
from django.shortcuts import render
from .services.models import Encounter, HarmReduction
from .clients.models import Person, Client
from django.db.models import Max, Min, Sum, Count
import datetime
from .syringes.models import SyringeCollection




class PersonModelList(ModelList):
    template = 'dashboard/person_model_list.html'


class Statistics(DashboardModule):
        template = 'dashboard/first_column.html'


class FirstDate(DashboardModule):
        template = 'dashboard/second_column.html'






class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        user = context['request'].user

        self.first = Encounter.objects.order_by('performed_on')[0].performed_on

        self.count_syringe = HarmReduction.objects.aggregate(Sum('out_count')).get('out_count__sum', 0.00)

        self.top_clients_by_enc = Client.objects.annotate(num_id=Count('encounters')).order_by('-num_id')[:5]

        self.all_clients = Client.objects.aggregate(Count('id')).get('id__count', 0.00)

        clients = Client.objects.annotate(num_in=Sum('encounters__services__harmreduction__in_count'), num_out=Sum('encounters__services__harmreduction__out_count'))
        for client in clients:
            client.num_diff = (client.num_out or 0) - (client.num_in or 0)
        self.top_clients_by_syringe_diff = sorted(clients, lambda a, b: abs(b.num_diff) - abs(a.num_diff))[:5]


        year = datetime.datetime.today().year - 1
        month = datetime.datetime.today().month

        self.encounters = []
        self.persons = []
        self.syringe = []
        person_count = Client.objects.filter(created__lt=datetime.date(year, month, 1)).count()
        for i in range(12):
            month += 1
            if month == 13:
                month = 1
                year += 1
            print "%s: %s" % (year, month)
            syringe_count = 0
            enc_count = Encounter.objects.filter(performed_on__month=month,
                                     performed_on__year=year).count()
            person_count = Client.objects.filter(created__month=month, created__year=year).count()
            syringe_count += HarmReduction.objects.filter(encounter__performed_on__month=month,
                                                          encounter__performed_on__year=year).aggregate(
                Sum('out_count')).get('out_count__sum', 0.00) or 0
            syringe_count += HarmReduction.objects.filter(encounter__performed_on__month=month,
                                                          encounter__performed_on__year=year).aggregate(
                Sum('in_count')).get('in_count__sum', 0.00) or 0
            self.encounters.append(enc_count)
            self.persons.append(person_count)
            self.syringe.append(syringe_count)
        self.months = ['Led', 'Uno', 'Bre', 'Dub', 'Kve', 'Crv', 'Crn', 'Srp', 'Zar', 'Rij',
                       'Lis', 'Pro']

        self.months = self.months[month:] + self.months[:month]



        #pocet novych klientu
        self.children.append(Statistics(
            _('Statistika'),
            limit=6,
            collapsible=False,
            column=1,
        ))

        self.children.append(FirstDate(
            _('Datum prvniho kontaktu'),
            limit=6,
            collapsible=False,
            column=2,

        ))
        self.children.append(PersonModelList(
            _(u'Databáze osob'),
            collapsible=False,
            column=1,
            models=(
                'boris.clients.models.Client',
                'boris.clients.models.Anonymous',
            ),
        ))

        models = ('boris.services.models.core.Encounter', 'boris.clients.models.Anamnesis',
                  'boris.clients.models.PractitionerContact', 'boris.clients.models.GroupContact',
                  'boris.syringes.models.SyringeCollection', 'boris.clients.models.TerrainNotes',)

        self.children.append(modules.ModelList(
            _(u'Rychlé akce'),
            collapsible=False,
            column=1,
            models=models,
        ))

        if user.is_superuser:
            # append an app list module for "Administration"
            self.children.append(modules.ModelList(
                _(u'Administrace'),
                column=1,
                collapsible=True,
                css_classes=('grp-collapse grp-closed',),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _(u'Výstupy'),
            column=3,
            collapsible=False,
            children=[
                {
                    'title': _(u'Vytvořit výstup měst'),
                    'url': reverse('reporting_towns'),
                    'external': False,
                },
                {
                    'title': _(u'Vytvořit výstup výkonů'),
                    'url': reverse('reporting_services'),
                    'external': False,
                },
                {
                    'title': _(u'Vytvořit výstup klientů'),
                    'url': reverse('reporting_clients'),
                    'external': False,
                },
                {
                    'title': _(u'Vytvořit výstup pro hygienu'),
                    'url': reverse('reporting_hygiene'),
                    'external': False,
                },
                {
                    'title': _(u'Vytvořit výstup pro RVKPP'),
                    'url': reverse('reporting_govcouncil'),
                    'external': False,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))




