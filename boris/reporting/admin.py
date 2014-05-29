# -*- coding: utf8 -*-

from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils.datastructures import SortedDict

from boris.reporting.core import ReportResponse
from boris.reporting import forms
from boris.reporting.reports.hygiene import HygieneReport
from boris.reporting.reports.monthly_stats import MonthlyStatsByTown, \
    MonthlyStatsByDistrict, StatsByTownInPeriod
from boris.reporting.reports.services import ServiceReport
from boris.reporting.reports.clients import ClientReport
from boris.reporting.reports.yearly_stats import YearlyStatsByMonth, YearlyStatsByTown, \
    YearlyStatsByDistrict
from boris.reporting.reports.council import GovCouncilReport


class ReportingInterfaceTab(object):
    """
    One tab of the interface. Requires 2 attributes to be set:
        `report`       Report subclass
        `form`         Form used to get parameters for report initiation
        `form prefix`  Prefix to separate forms' id namespaces on the rendered page.
    """
    report = None
    form = None
    form_prefix = None
    template = None

    @classmethod
    def get_urlname(cls):
        return 'reporting_%s' % cls.__name__.lower()

    def get_title(self):
        return self.report.title

    def get_description(self):
        return self.report.description

    def get_absolute_url(self):
        return reverse(self.get_urlname())


def interfacetab_factory(report_cls, form_cls, form_prefix, template='reporting/tab.html'):
    attrs = {'report': report_cls,
             'form': form_cls,
             'form_prefix': form_prefix,
             'template': template}

    cls = type(report_cls.__name__ + 'Tab',
               (ReportingInterfaceTab,),
               attrs)

    return cls


"""
Separate report forms are splitted to tabs in admin, this
class handles management of these forms.

Tabs are defined as ReportInterfaceTab subclasses listed in
`tabs` attribute.
"""

class TownReportingInterface(object):
    tabs = (
        interfacetab_factory(MonthlyStatsByTown, forms.MonthlyStatsForm, 'monthbytown'),
        interfacetab_factory(YearlyStatsByTown, forms.MonthlyStatsForm, 'yearbytown'),
        interfacetab_factory(MonthlyStatsByDistrict, forms.MonthlyStatsForm, 'monthbydistrict'),
        interfacetab_factory(YearlyStatsByDistrict, forms.MonthlyStatsForm, 'yearbydistrict'),
        interfacetab_factory(StatsByTownInPeriod, forms.BaseReportForm, 'yearbydistrict'),
    )


class ServicesReportingInterface(object):
    tabs = (
        interfacetab_factory(ServiceReport, forms.ServiceForm, 'services'),
    )


class ClientsReportingInterface(object):
    tabs = (
        interfacetab_factory(ClientReport, forms.BaseReportForm, 'clients'),
    )

class GovCouncilReportingInterface(object):
    tabs = (
        interfacetab_factory(GovCouncilReport, forms.GovCouncilForm, 'govcouncil'),
    )


class HygieneReportingInterface(object):
    tabs = (
        interfacetab_factory(HygieneReport, forms.HygieneForm, 'hygiene'),
    )


class ReportingInterfaceHandler(object):
    """Class-based view for showing reporting interface."""
    id = 'base'
    title = None
    interface_class = None

    def __call__(self, request, tab_class=None):
        interface = self.interface_class()
        tabs = SortedDict()

        for t in interface.tabs:
            tab = t()
            if tab_class == t and request.method == 'POST':
                form = tab.form(request.POST, prefix=tab.form_prefix)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    display_type = cleaned_data.pop('display')

                    return ReportResponse(tab.report,
                                          request,
                                          display_type,
                                          **cleaned_data)
            else:
                form = tab.form(prefix=tab.form_prefix)
            tabs[tab] = form

        ctx = {'tabs': tabs.items(), 'interface': interface, 'name': self.title}
        return render(request, 'reporting/interface.html', ctx)

    def get_urls(self):
        """
        Returns all urls for interface. Each tab has it's own POST URL plus
        there is one extra URL for base view.
        """

        interface = self.interface_class()

        urlpatterns = patterns('',
            url('^$', admin.site.admin_view(self.__call__, cacheable=True),
                name='reporting_%s' % self.id)
        )

        for t in interface.tabs:
            urlpatterns += patterns('',
                url(r'^%s/$' % slugify(t.__name__), admin.site.admin_view(
                            self.__call__, cacheable=False),
                    kwargs={'tab_class': t}, name=t.get_urlname())
            )

        return urlpatterns, 'reporting', None
    urls = property(get_urls)


class TownReportingInterfaceHandler(ReportingInterfaceHandler):
    id = 'towns'
    title = u'Města'
    interface_class = TownReportingInterface


class ServicesReportingInterfaceHandler(ReportingInterfaceHandler):
    id = 'services'
    title = u'Výkony'
    interface_class = ServicesReportingInterface


class ClientReportingInterfaceHandler(ReportingInterfaceHandler):
    id = 'clients'
    title = u'Klienti'
    interface_class = ClientsReportingInterface


class HygieneReportingInterfaceHandler(ReportingInterfaceHandler):
    id = 'hygiene'
    title = u'Hygiena'
    interface_class = HygieneReportingInterface

class GovCouncilReportingInterfaceHandler(ReportingInterfaceHandler):
    id = 'govcouncil'
    title = u'RVKPP'
    interface_class = GovCouncilReportingInterface



towns = TownReportingInterfaceHandler()
services = ServicesReportingInterfaceHandler()
clients = ClientReportingInterfaceHandler()
hygiene = HygieneReportingInterfaceHandler()
govcouncil = GovCouncilReportingInterfaceHandler()
