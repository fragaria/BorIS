# -*- coding: utf8 -*-

from boris.impact import forms

from boris.impact.reports.impact import ImpactClient, ImpactAnamnesis
from boris.reporting.admin import interfacetab_factory, ReportingInterfaceHandler

"""
Separate report forms are splitted to tabs in admin, this
class handles management of these forms.

Tabs are defined as ReportInterfaceTab subclasses listed in
`tabs` attribute.
"""
class ImpactReportingInterface(object):
    tabs = (
        interfacetab_factory(ImpactClient, forms.ImpactForm, 'client'),
        interfacetab_factory(ImpactAnamnesis, forms.ImpactForm, 'anamnesis'),
    )


class ImpactInterfaceHandler(ReportingInterfaceHandler):
    """Class-based view for showing impact interface."""
    id = 'base'
    title = None
    interface_class = None
    url_title = 'impact'


class ImpactReportingInterfaceHandler(ImpactInterfaceHandler):
    id = 'impact'
    title = u'Dopadová studie'
    interface_class = ImpactReportingInterface


impact = ImpactReportingInterfaceHandler()
