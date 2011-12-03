from collections import defaultdict

from django.http import HttpResponse
from django.template import loader


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
    def __init__(self, report_class, *args, **kwargs):
        report = report_class(*args, **kwargs)
        super(ReportResponse, self).__init__(content=report.render(), mimetype=report.mime)
        self['Content-Disposition'] = 'attachment; filename=report.xls'


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

            if self.filtering:
                qset = qset.filter(self._filtering)

            if self.excludes:
                qset = qset.exclude(self._excludes)

            self._vals = defaultdict(int)
            
            vals = qset.values(*self.get_grouping()).order_by().annotate(
                    total=self.get_annotation_func())

            for value in vals:
                key = make_key((k, value[k]) for k in self.get_grouping())
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
    
    def get_grouping(self):
        """
        Overload this to enable custom grouping (different from report's) for
        Aggregation subclass
        """
        return self.report.grouping

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
