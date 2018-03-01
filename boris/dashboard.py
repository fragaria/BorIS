# -*- coding: utf-8 -*-

import datetime
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import ModelList, DashboardModule

from boris.clients.models import Client
from boris.services.models import Encounter, HarmReduction


class PersonModelList(ModelList):
    template = 'dashboard/person_model_list.html'


class StatisticFirstColumn(DashboardModule):
    template = 'dashboard/first_column.html'


class StatisticSecondColumn(DashboardModule):
    template = 'dashboard/second_column.html'


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def __init__(self, **kwargs):
        super(CustomIndexDashboard, self).__init__(**kwargs)

        self.encounters = []
        self.persons = []
        self.syringe = []
        self.months = ['Led', 'Úno', 'Bře', 'Dub', 'Kvě', 'Črv', 'Črn', 'Srp', 'Zář', 'Říj', 'Lis', 'Pro']

        clients = Client.objects.annotate(num_in=Sum('encounters__services__harmreduction__in_count'),
                                          num_out=Sum('encounters__services__harmreduction__out_count'))
        for client in clients:
            client.num_diff = (client.num_in or 0) - (client.num_out or 0)

        self.top_clients_by_syringe_diff = sorted(clients, lambda a, b: abs(b.num_diff) - abs(a.num_diff))[:5]
        self.all_clients = Client.objects.aggregate(Count('id')).get('id__count', 0)
        self.top_clients_by_enc = Client.objects.annotate(enc_count=Count('encounters')).order_by('-enc_count')[:5]
        self.count_syringe = HarmReduction.objects.aggregate(Sum('out_count')).get('out_count__sum', 0)
        self.first_contact = Encounter.objects.order_by('performed_on')[0] if Encounter.objects.order_by('performed_on') else None

    def init_with_context(self, context):
        user = context['request'].user

        year = datetime.datetime.today().year - 1
        month = datetime.datetime.today().month

        for i in range(12):
            month += 1
            if month == 13:
                month = 1
                year += 1

            enc_count = Encounter.objects.filter(performed_on__month=month, performed_on__year=year).count()
            person_count = Client.objects.filter(created__month=month, created__year=year).count()

            syringe_count = HarmReduction.objects.filter(encounter__performed_on__month=month,
                                                         encounter__performed_on__year=year).aggregate(
                                                            Sum('out_count')).get('out_count__sum', 0) or 0

            self.encounters.append(enc_count)
            self.persons.append(person_count)
            self.syringe.append(syringe_count)

        self.months = self.months[month:] + self.months[:month]

        self.children.append(StatisticFirstColumn(
            collapsible=False,
            column=1,
        ))

        self.children.append(StatisticSecondColumn(
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
                # {
                #     'title': _(u'Vytvořit dopadovou studii'),
                #     'url': reverse('reporting_impact'),
                #     'external': False,
                # },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


