from collections import defaultdict

from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext


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
    def __init__(self, report_class, request, *args, **kwargs):
        report = report_class(*args, **kwargs)
        super(ReportResponse, self).__init__(content=report.render(request),
                                             content_type=report.contenttype)
        if report.response_headers:
            self.__dict__.update(report.response_headers)


class BaseReport(object):
    title = None
    description = None
    contenttype = 'application/vnd.ms-excel; charset=utf-8'
    response_headers = {
        'Content-Disposition': 'attachment; filename=report.xls'
    }


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

    @property
    def contenttype(self):
        return 'application/vnd.ms-excel; charset=utf-8'

    @property
    def template(self):
        return (
            'reporting/reports/%s.html' % self.__class__.__name__.lower(),
        )

    def get_context(self):
        return {'report': self}

    def render(self, request):
        return loader.render_to_string(
            self.template,
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
                vals = qset.values(*grouping).order_by().annotate(
                        total=self.get_annotation_func())

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


class SumAggregation(Aggregation):
    """
    Row that uses SUM instead of COUNT to aggregate.
    """
    def get_annotation_func(self):
        from django.db.models import Sum
        return Sum(self.aggregation_dbcol)


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
