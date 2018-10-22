from collections import defaultdict

from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext

from boris.reporting.forms import OUTPUT_BROWSER, OUTPUT_OFFICE


class hashdict(dict):
    """
    A dict that is hashable. BEWARE not to mutate it..
    """
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def make_key(expression):
    return hashdict(expression)


class ReportResponse(HttpResponse):
    """
    Ancestor of HttpRespose which takes report class and its args and kwargs
    that renders itself.
    """
    def __init__(self, report_class, request, display_type, *args, **kwargs):
        report = report_class(*args, **kwargs)
        content = report.render(request, display_type)
        super(ReportResponse, self).__init__(content=content,
                                             content_type=report.contenttype(display_type))
        if report.response_headers(display_type):
            for key, val in report.response_headers(display_type).items():
                self[key] = val


class BaseReport(object):
    title = None
    description = None
    contenttype_office = 'application/vnd.ms-excel; charset=utf-8'
    browser_only = False
    template_path = 'reporting'

    def get_filename(self):
        return 'report.xls'

    def contenttype(self, display_type):
        if self.browser_only:
            return 'text/html'

        return {
            OUTPUT_BROWSER: 'text/html',
            OUTPUT_OFFICE: self.contenttype_office,
        }[display_type]

    def response_headers(self, display_type):
        if self.browser_only:
            return {}

        return {
            OUTPUT_BROWSER: {},
            OUTPUT_OFFICE: {
                'Content-Disposition': 'attachment; filename=%s' % self.get_filename()
            }
        }[display_type]

    def get_template(self, display_type):
        if self.browser_only:
            return '%s/reports/%s_browser.html' % (self.template_path, self.__class__.__name__.lower())

        return (
            '%s/reports/%s_%s.html' % (self.template_path, self.__class__.__name__.lower(),
                display_type),  # display_type can be "browser" or "office"
        )


class Report(BaseReport):
    """
    Base class for reporting output.

    Subclasses might (or must) specify the following attributes:

    - columns (required) - column titles for the rendered tables
    - grouping (required)
    - grouping_total (required) - grouping for the last report column ("Total")
    - additional_filtering (optional)
    - additional_excludes (optional)

    and methods:

    - get_data (required) - returns the data to be used in the template
    """
    columns = None
    aggregation_classes = ()

    def __unicode__(self):
        return self.title

    def get_context(self):
        return {'report': self}

    def render(self, request, display_type):
        return loader.render_to_string(
            self.get_template(display_type),
            self.get_context(),
            context_instance=RequestContext(request))

    @property
    def aggregations(self):
        if not hasattr(self, '_aggregations'):
            self._aggregations = [aggregation_class(self) for aggregation_class in self.aggregation_classes]
        return self._aggregations

    def get_data(self, *args, **kwargs):
        raise NotImplementedError


class Aggregation(object):
    """
    Main reporting logic lives in AggregationRow. It does aggregation
    on queryset specified by report.

    Subclasses can supply filtering/excluding, grouping and column, which
    should be treated as distinct (the one to report on).
    """
    filtering = {}
    excludes = {}
    aggregation_dbcol = 'id'
    model = None

    def __init__(self, report):
        self._filtering = self._prepare_expression(self.filtering)
        self._excludes = self._prepare_expression(self.excludes)

        if hasattr(report, 'additional_filtering'):
            self._filtering = self._filtering & self._prepare_expression(report.additional_filtering)
        if hasattr(report, 'additional_excludes'):
            self._excludes = self._excludes & self._prepare_expression(report.additional_excludes)
        self.report = report

    def _values(self):
        if not hasattr(self, '_vals'):
            qset = self.model.objects.all()

            if self._filtering:
                qset = qset.filter(self._filtering)

            if self._excludes:
                qset = qset.exclude(self._excludes)

            self._vals = defaultdict(int)

            for grouping in (self.report.grouping, self.report.grouping_total):
                vals = qset.values(*grouping).order_by().annotate(total=self.get_annotation_func())

                for value in vals:
                    key = make_key((k, value[k]) for k in grouping)
                    # non-existent entries return None, hence "or 0"
                    self._vals[key] += value['total'] or 0

        return self._vals

    def _prepare_expression(self, qset_expression):
        from django.db.models import Q
        if isinstance(qset_expression, dict):
            return Q(**qset_expression)
        else:
            return qset_expression

    def get_annotation_func(self):
        """
        Function to create reporting on. Defaults to COUNT.
        """
        from django.db.models import Count
        return Count(self.aggregation_dbcol, distinct=True)

    def get_val(self, key):
        """
        Return value for given column.
        """
        return self._values()[key]

    def get_total(self, key):
        return self.get_val(make_key(((key, 1),)))


class SumAggregation(Aggregation):
    """
    Row that uses SUM instead of COUNT to aggregate.
    """
    def get_annotation_func(self):
        from django.db.models import Sum
        return Sum(self.aggregation_dbcol)

    def get_total(self, key):
        """
        Return value for given column.
        SumAggregation total needs to be handled differently (sum of all grouping_constant values).
        """
        res = 0
        for val in self._values():
            if key in val:
                res += self._values()[val]
        return res


class NonDistinctCountAggregation(Aggregation):
    """
    Row that uses COUNT without distinct to annotate.
    """
    def get_annotation_func(self):
        from django.db.models import Count
        return Count(self.aggregation_dbcol, distinct=False)


class SuperAggregation(Aggregation):
    """ Provides an 'aggregation' (sum) over aggregations. """
    aggregation_classes = []

    def __init__(self, report):
        self.aggregations = [
            aggr_class(report) for aggr_class in self.aggregation_classes
        ]

    def get_val(self, key):
        return sum(aggregation.get_val(key) for aggregation in self.aggregations)
