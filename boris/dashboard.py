# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        user = context['request'].user

        self.children.append(modules.ModelList(
            _(u'Databáze osob'),
            collapsible=False,
            column=1,
            models=('boris.clients.models.Client', 'boris.clients.models.Practitioner'),
        ))

        self.children.append(modules.ModelList(
            _(u'Rychlé akce'),
            collapsible=False,
            column=1,
            models=(
                'boris.services.models.core.Encounter',
                'boris.clients.models.Anamnesis',
                'boris.other.models.SyringeCollection'
            ),
        ))

        if user.is_superuser:
            # append an app list module for "Administration"
            self.children.append(modules.ModelList(
                _(u'Administrace'),
                column=1,
                collapsible=True,
                css_classes=('collapse closed',),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _(u'Výstupy'),
            column=2,
            collapsible=False,
            children=[
                {
                    'title': _(u'Vytvořit výkaz'),
                    'url': reverse('reporting_base'),
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


