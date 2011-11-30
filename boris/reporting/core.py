from collections import defaultdict

from django.http import HttpResponse
from django.template import loader


class hashdict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class ReportResponse(HttpResponse):
    """
    Ancestor of HttpRespose which takes report class and its args and kwargs
    that renders itself.
    """
    def __init__(self, report_class, *args, **kwargs):
        report = report_class(*args, **kwargs)
        super(ReportResponse, self).__init__(content=report.render(), mimetype=report.mime)
        self['Content-Disposition'] = 'attachment; filename=report.csv'


class Report(object):
    """
    Base class for reporting output.

    Subclasses might (or must) specify the following attributes:

    - columns (required) - column titles for the rendered tables
    - grouping (required)
    - additional_filtering (optional)
    - additional_excludes (optional)

    and methods:

    - get_data (required) - returns the data to be used in the template
    """
    title = None
    columns = None
    aggregation_classes = ()

    def __unicode__(self):
        return self.title

    @property
    def mime(self):
        return 'application/vnd.ms-excel'

    @property
    def template(self):
        return (
            'reporting/reports/%s.html' % self.__class__.__name__.lower(),
        )

    def get_context(self):
        return {'report': self}

    def render(self):
        return loader.render_to_string(self.template, self.get_context())

    @property
    def aggregations(self):
        if not hasattr(self, '_aggregations'):
            self._aggregations = [aggregation_class(self) for aggregation_class in self.aggregation_classes]
        return self._aggregations


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
        if hasattr(report, 'additional_filtering'):
            self.filtering.update(report.additional_filtering)
        if hasattr(report, 'additional_excludes'):
            self.excludes.update(report.additional_excludes)
        self.report = report
        self.grouping = report.grouping

    def _values(self):
        if not hasattr(self, '__values'):
            qset = self.model.objects.all()

            if self.filtering:
                qset = qset.filter(**self.filtering)

            if self.excludes:
                qset = qset.exclude(**self.excludes)

            self.__values = defaultdict(int)
            vals = qset.values(*self.grouping).order_by().annotate(
                    total=self._annotation_func())

            for value in vals:
                key = hashdict((k, value[k]) for k in self.grouping)
                self.__values[key] += value['total']

        return self.__values

    def _annotation_func(self):
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
    def _annotation_func(self):
        from django.db.models import Sum
        return Sum(self.aggregation_dbcol)
