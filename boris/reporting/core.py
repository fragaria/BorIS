'''
Created on 20.11.2011

@author: xaralis
'''
from django.http import HttpResponse
from django.template import loader


class ReportResponse(HttpResponse):
    def __init__(self, report_class, *args, **kwargs):
        report = report_class(*args, **kwargs)
        super(ReportResponse, self).__init__(content=report.render(), mimetype=report.mime)


class Report(object):
    title = None
    columns = None
    rows = None

    @property
    def mime(self):
        return 'application/vnd.ms-excel'

    @property
    def template(self):
        return (
            'reporting/reports/%s.html' % self.__class__.__name__.lower(),
            'reporting/reports/default.html'
        )
        
    def __unicode__(self):
        return self.title
    
    def get_context(self):
        return {'report': self}
    
    def render(self):
        return loader.render_to_string(self.template, self.get_context())


class Column(object):
    def __init__(self, report, key, title=None):
        self.report = report
        self.key = key
        if title is None:
            self.title = unicode(self.key)
        else:
            self.title = title
            
    def __unicode__(self):
        return  self.title
            
    def get_key(self):
        return self.key
    
    
class Row(object):
    def __init__(self, report, title=None):
        self.report = report
        if title is not None:
            self.title = title
    
    def __unicode__(self):
        return unicode(self.title)
    
    def get_val(self, column):
        return NotImplementedError
    
    
class QuerySetReport(Report):
    row_classes = ()
    column_class = Column
    column_keys = ()

    def _columns(self):
        if not hasattr(self, '__columns'):
            self.__columns =  [self.column_class(self, key, title=self.column_title(key))
                for key in self.column_keys]
        return self.__columns
    columns = property(_columns)
    
    def column_title(self, key):
        return unicode(key)
    
    def _rows(self):
        if not hasattr(self, '__rows'):
            self.__rows = [RowClass(self) for RowClass in self.row_classes]
        return self.__rows
    rows = property(_rows)
    
    def __init__(self, *args, **kwargs):
        self.base_qset = self.get_base_qset()
    
    def get_base_qset(self):
        return None
    
    
class AggregationRow(Row):
    base_qset = None
    additional_filtering = {}
    additional_excludes = {}
    grouping = ()
    distinct_val = 'id'
    
    def set_base_qset(self, base_qset):
        self.base_qset = base_qset 
        
    def set_grouping(self, grouping):
        self.grouping = grouping
    
    def _values(self):
        from django.db.models import Count
        if not hasattr(self, '__values'):
            qset = self.report.base_qset
            
            if self.additional_filtering:
                qset = qset.filter(**self.additional_filtering)
                
            if self.additional_excludes:
                qset = qset.exclude(**self.additional_excludes)
            
            self.__values = qset.values(*self.report.grouping).order_by().annotate(
                    total=self._annotation_func())
        return self.__values
    
    def _annotation_func(self):
        from django.db.models import Count
        return Count(self.distinct_val, distinct=True)
    
    def itervalues(self):
        for column in self.report.columns:
            yield self.get_val(column)
    
    def get_val(self, column):
        def entry_ok(entry):
            for key in column.get_key():
                if entry[key] != column.get_key()[key]:
                    return False
            return True

        return sum(val['total'] for val in self._values() if entry_ok(val))
        
class SumAggregationRow(AggregationRow):
    def _annotation_func(self):
        from django.db.models import Sum
        return Sum(self.distinct_val)
    
    