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
    description = _(u'Statistika zobrazuje data agregovaná za všechny města po měsících.')
    grouping = ('month',)
    grouping_total = ('year',)

    def get_filename(self):
        return 'stat_rocni.xls'

    def _columns(self):
        return self.months()
    columns = property(_columns)

    def get_sum(self, aggregation):
        return aggregation.get_val(make_key((('year', self.year),)))

    def get_data(self):
        return [
            (aggregation.title, [
                aggregation.get_val(
                    make_key((('month', month),))
                ) for month in self.columns
            ] + [self.get_sum(aggregation)]) for aggregation in self.aggregations
        ]
