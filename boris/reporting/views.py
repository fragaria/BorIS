# -*- encoding: utf-8 -*-

from django.db.models import Count
from boris.reporting.reports.monthly_stats import MonthlyStats
from boris.reporting.core import ReportResponse

class Aggregation(object):
    """
    Holds and searches through aggregated data.

    Arguments:
        - model: what model the data comes from
        - group_by: group by these values
        - distinct_val: count distinct values of <distinct_val> in each group
    """
    def __init__(self, model, filter_dict, group_by, distinct_val='id', title='Cube'):
        values = model.objects.filter(**filter_dict).values(*group_by)
        self.values = values.order_by().annotate(total=Count(distinct_val, distinct=True))
        self.title = title

    def total(self, filter_criteria={}):
        """
        Get the sum of totals in entries fulfilling the <filter_criteria>.
        """
        def entry_ok(entry):
            for key in filter_criteria:
                if entry[key] != filter_criteria[key]:
                    return False
            return True

        return sum(val['total'] for val in self.values if entry_ok(val))

    def __unicode__(self):
        return self.title


def monthly_stats(request):
    return ReportResponse(MonthlyStats, 2011)
