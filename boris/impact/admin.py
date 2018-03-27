# -*- coding: utf8 -*-

from django.conf.urls import url, patterns
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils.datastructures import SortedDict

from boris.reporting.core import ReportResponse
from boris.impact import forms

from boris.impact.reports.impact import ImpactReport, ImpactTimeseries, ImpactClient, ImpactAnamnesis
from boris.reporting.admin import interfacetab_factory

"""
Separate report forms are splitted to tabs in admin, this
class handles management of these forms.

Tabs are defined as ReportInterfaceTab subclasses listed in
`tabs` attribute.
"""
class ImpactReportingInterface(object):
    tabs = (
        # interfacetab_factory(ImpactTimeseries, forms.ReportForm, 'timeseries'),
        interfacetab_factory(ImpactClient, forms.ImpactForm, 'client'),
        interfacetab_factory(ImpactAnamnesis, forms.ImpactForm, 'anamnesis'),
    )


class ImpactInterfaceHandler(object):
    """Class-based view for showing impact interface."""
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
                name='impact_%s' % self.id)
        )

        for t in interface.tabs:
            urlpatterns += patterns('',
                url(r'^%s/$' % slugify(t.__name__), admin.site.admin_view(
                            self.__call__, cacheable=False),
                    kwargs={'tab_class': t}, name=t.get_urlname())
            )

        return urlpatterns, 'impact', None
    urls = property(get_urls)


class ImpactReportingInterfaceHandler(ImpactInterfaceHandler):
    id = 'impact'
    title = u'Dopadová studie'
    interface_class = ImpactReportingInterface


impact = ImpactReportingInterfaceHandler()
