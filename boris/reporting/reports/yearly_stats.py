# -*- encoding: utf-8 -*-
'''
Created on 4.12.2011

@author: xaralis
'''
from django.utils.translation import ugettext as _

from boris.reporting.core import make_key

from .monthly_stats import MonthlyStatsByTown

class YearlyStatsByMonth(MonthlyStatsByTown):
    title = _(u'Roční statistiky po měsících')
    grouping = ('month',)
    
    def _columns(self):
        return self.months()
    columns = property(_columns)
    
    def get_sum(self, aggregation):
        return sum(
            aggregation.get_val(make_key((('month', month),)))
            for month in self.columns
        )
    
    def get_data(self):
        return [
            (aggregation.title, [
                aggregation.get_val(
                    make_key((('month', month),))
                ) for month in self.columns
            ] + [self.get_sum(aggregation)]) for aggregation in self.aggregations
        ]