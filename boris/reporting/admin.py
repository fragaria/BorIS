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
    MonthlyStatsByDistrict
from boris.reporting.reports.services import ServiceReport
from boris.reporting.reports.clients import ClientReport
from boris.reporting.reports.yearly_stats import YearlyStatsByMonth


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


class ReportingInterface(object):
    """
    Separate report forms are splitted to tabs in admin, this
    class handles management of these forms.

    Tabs are defined as ReportInterfaceTab subclasses listed in
    `tabs` attribute.
    """
    tabs = (
        interfacetab_factory(MonthlyStatsByTown, forms.MonthlyStatsForm, 'monthbytown'),
        interfacetab_factory(MonthlyStatsByDistrict, forms.MonthlyStatsForm, 'monthbydistrict'),
        interfacetab_factory(YearlyStatsByMonth, forms.MonthlyStatsForm, 'yearbymonth'),
        interfacetab_factory(ServiceReport, forms.ServiceForm, 'services'),
        interfacetab_factory(ClientReport, forms.BaseReportForm, 'clients'),
        interfacetab_factory(HygieneReport, forms.HygieneForm, 'hygiene'),
    )


class ReportingInterfaceHandler(object):
    """Class-based view for showing reporting interface."""

    def __call__(self, request, tab_class=None):
        interface = ReportingInterface()
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

        ctx = {'tabs': tabs.items(), 'interface': interface}
        return render(request, 'reporting/interface.html', ctx)

    def get_urls(self):
        """
        Returns all urls for interface. Each tab has it's own POST URL plus
        there is one extra URL for base view.
        """

        interface = ReportingInterface()

        urlpatterns = patterns('',
            url('^$', admin.site.admin_view(self.__call__, cacheable=True),
                name='reporting_base')
        )

        for t in interface.tabs:
            urlpatterns += patterns('',
                url(r'^%s/$' % slugify(t.__name__), admin.site.admin_view(
                            self.__call__, cacheable=False),
                    kwargs={'tab_class': t}, name=t.get_urlname())
            )

        return urlpatterns, 'reporting', None
    urls = property(get_urls)

interface = ReportingInterfaceHandler()

