# -*- encoding: utf-8 -*-
'''
Created on 4.12.2011

@author: xaralis
'''
from django.utils.translation import ugettext as _

from boris.reporting.core import make_key

from .monthly_stats import MonthlyStatsByTown

class YearlyStatsByTown(MonthlyStatsByTown):
    title = _(u'Roční statistiky podle města')
    grouping = ('year', 'town')
    
    def get_data(self):
        return [
            (year, [
                (aggregation.title, [
                    aggregation.get_val(
                        make_key((('year', year), ('town', town.pk)),)
                    ) for town in self.columns
                ]) for aggregation in self.aggregations
            ]) for year in [self.year,]
        ]