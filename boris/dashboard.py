# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import ModelList
from boris import settings


class PersonModelList(ModelList):
    template = 'dashboard/person_model_list.html'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        user = context['request'].user

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
                  'boris.syringes.models.SyringeCollection',)

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
            column=2,
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


