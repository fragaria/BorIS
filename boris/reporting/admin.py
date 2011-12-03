# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

from django.utils.translation import ugettext_lazy as _

from boris.reporting.reports.monthly_stats import MonthlyStats
from boris.reporting.core import ReportResponse
from boris.reporting.forms import MonthlyStatsForm

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.shortcuts import render


class ReportingInterfaceTab(object):
    """
    One tab of the interface. Requires 3 attributes to be set:
        `title`        Tab's title
        `report`       Report subclass
        `form`         Form used to get parameters for report initiation
    """
    title = _(u'Výkaz')
    report = None
    form = None
    
    @classmethod
    def get_urlname(cls):
        return 'reporting_%s' % cls.__name__.lower()
    
    def get_absolute_url(self):
        return reverse(self.get_urlname())
    

class MonthlyStatsTab(ReportingInterfaceTab):
    title = _(u'Měsíční statistiky')
    report = MonthlyStats
    form = MonthlyStatsForm


class ReportingInterface(object):
    """
    Class-based view for showing reporting interface.
    
    Separate report forms are splitted to tabs in admin, this
    class handles management of these forms.
    
    Tabs are defined as ReportInterfaceTab subclasses listed in 
    `tabs` attribute.
    """
    tabs = (
        MonthlyStatsTab,
    )
    
    def __call__(self, request, tab_class=None):
        ctx = {'tabs': {}}
        for t in self.tabs:
            if tab_class == t and request.method == 'POST':
                form = t.form(request.POST)
                if form.is_valid():
                    return ReportResponse(t.report, **form.cleaned_data)
            else:
                form = t.form()
            ctx['tabs'][t] = form
        
        return render(request, 'reporting/interface.html', ctx)
    
    def get_urls(self):
        """
        Returns all urls for interface. Each tab has it's own POST URL.
        """
        urlpatterns = patterns('boris.reporting.admin',
            url('^$', 'interface', name='reporting_base')
        )
        
        for t in self.tabs:
            urlpatterns += patterns('boris.reporting.admin',
                url(r'^%s/$' % slugify(t.__name__), 'interface',
                    kwargs={'tab_class': t}, name=t.get_urlname())
            )
        
        return urlpatterns, 'reporting', None
    urls = property(get_urls)

interface = ReportingInterface()

