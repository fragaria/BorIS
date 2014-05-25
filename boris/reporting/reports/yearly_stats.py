# -*- encoding: utf-8 -*-
from django.utils.translation import ugettext as _

from boris.reporting.core import make_key

from .monthly_stats import MonthlyStatsByTown, MonthlyStatsByDistrict


class YearlyStatsByTown(MonthlyStatsByTown):
    title = _(u'Roční')
    description =  _(u'Statistika podle <strong>měst</strong> v celkovém součtu za zvolený rok.')
    grouping = ('year', 'town')
    grouping_total = ('year',)

    def get_filename(self):
        return 'stat_rocni_podle_mesta.xls'

    def get_data(self):
        return [
            (aggregation.title, [
                aggregation.get_val(
                    make_key((('year', self.year), ('town', town.pk)))
                ) for town in self.columns
            ] + [aggregation.get_val(make_key((('year', self.year),)))]) for aggregation in self.aggregations
        ]


class YearlyStatsByDistrict(MonthlyStatsByDistrict):
    title = _(u'Okresy: roční')
    description =  _(u'Statistika podle <strong>okresů</strong> v celkovém součtu za zvolený rok.')
    grouping = ('year', 'town__district')
    grouping_total = ('year',)

    def get_filename(self):
        return 'stat_rocni_podle_okresu.xls'

    def get_data(self):
        return [
            (aggregation.title, [
                aggregation.get_val(
                    make_key((('year', self.year), ('town__district', district.pk)))
                ) for district in self.columns
            ] + [aggregation.get_val(make_key((('year', self.year),)))]) for aggregation in self.aggregations
        ]


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
