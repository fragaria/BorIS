from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import formats
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.template import Library

from boris.services.models import IncomeExamination

register = Library()


def filter_dates(dates, year, month=None):
    """
    Filter dates by the given year and month.

    """
    try:
        year = int(year)
        month = int(month) if month else None
    except ValueError:
        return []
    return [
        date for date in dates
        if date.year == year and (date.month == month or not month)
    ]


@register.inclusion_tag('admin/date_hierarchy.html')
def related_date_hierarchy(cl, field_name):
    """
    Date hierarchy tag for client encounter dates.

    Slightly adapted date_hierarchy template tag from
    django/contrib/admin/templatetags/admin_list.py.

    """
    dates_or_datetimes = 'dates' # Only works with date fields.

    year_field = '%s__year' % field_name
    month_field = '%s__month' % field_name
    day_field = '%s__day' % field_name
    field_generic = '%s__' % field_name
    year_lookup = cl.params.get(year_field)
    month_lookup = cl.params.get(month_field)
    day_lookup = cl.params.get(day_field)

    link = lambda filters: cl.get_query_string(filters, [field_generic])

    if not (year_lookup or month_lookup or day_lookup):
        # select appropriate start level
        date_range = {
            'first': __border_date(cl, min),
            'last': __border_date(cl, max)
        }
        if date_range['first'] and date_range['last']:
            if date_range['first'].year == date_range['last'].year:
                year_lookup = date_range['first'].year
                if date_range['first'].month == date_range['last'].month:
                    month_lookup = date_range['first'].month

    if year_lookup and month_lookup and day_lookup:
        day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
        return {
            'show': True,
            'back': {
                'link': link({year_field: year_lookup, month_field: month_lookup}),
                'title': capfirst(formats.date_format(day, 'YEAR_MONTH_FORMAT'))
            },
            'choices': [{'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))}]
        }
    elif year_lookup and month_lookup:
        days = cl.queryset.filter(**{year_field: year_lookup, month_field: month_lookup})
        days = filter(bool, getattr(days, dates_or_datetimes)(field_name, 'day'))
        # Dates need to be filtered because of the 1:n relationship
        # (e.g. one client has multiple associated encounters.)
        days = filter_dates(days, year_lookup, month_lookup)
        return {
            'show': True,
            'back': {
                'link': link({year_field: year_lookup}),
                'title': str(year_lookup)
            },
            'choices': [{
                'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}),
                'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))
            } for day in days]
        }
    elif year_lookup:
        months = cl.queryset.filter(**{year_field: year_lookup})
        months = filter(bool, getattr(months, dates_or_datetimes)(field_name, 'month'))
        months = filter_dates(months, year_lookup)
        return {
            'show': True,
            'back': {
                'link': link({}),
                'title': _('All dates')
            },
            'choices': [{
                'link': link({year_field: year_lookup, month_field: month.month}),
                'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
            } for month in months]
        }
    else:
        years = __valid_years(cl, dates_or_datetimes, field_name)
        return {
            'show': True,
            'choices': [{
                'link': link({year_field: str(year.year)}),
                'title': str(year.year),
            } for year in years]
        }


def __valid_years(cl, dates_or_datetimes, field_name):
    opts = dict(cl.params)
    first_encounter = opts.pop('first_encounter', None)  # remove from filter
    if first_encounter == 'ano':
        return filter(bool, getattr(IncomeExamination.objects.filter(**opts), dates_or_datetimes)('encounter__performed_on', 'year'))
    if first_encounter == 'ne':
        return filter(bool, getattr(IncomeExamination.objects.filter(**opts), dates_or_datetimes)('encounter__performed_on', 'year'))
    return filter(bool, getattr(cl.queryset, dates_or_datetimes)(field_name, 'year'))


def __border_date(cl, fn):
    opts = dict(cl.params)
    first_encounter = opts.pop('first_encounter', None)  # remove from filter
    if first_encounter == 'ano':
        return fn([d for d in IncomeExamination.objects.filter(**opts).values_list('encounter__performed_on', flat=True) if d])
    if first_encounter == 'ne':
        return fn([d for d in IncomeExamination.objects.exclude(**opts).values_list('encounter__performed_on', flat=True) if d])
    return fn([d for d in cl.queryset.values_list('encounters__performed_on', flat=True) if d])
