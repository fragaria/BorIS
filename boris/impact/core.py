from collections import defaultdict

from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext

from boris.reporting.forms import OUTPUT_BROWSER, OUTPUT_OFFICE
from boris.reporting.core import BaseReport, ReportResponse

class hashdict(dict):
    """
    A dict that is hashable. BEWARE not to mutate it..
    """
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def make_key(expression):
    return hashdict(expression)


class BaseImpact(BaseReport):

    def get_filename(self):
        return 'impact.xls'

    def get_template(self, display_type):
        if self.browser_only:
            return ('impact/reports/%s_browser.html' % (self.__class__.__name__.lower()))

        return (
            'impact/reports/%s_%s.html' % (self.__class__.__name__.lower(),
                display_type), # display_type can be "browser" or "office"
        )



