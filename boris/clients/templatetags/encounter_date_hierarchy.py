from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import formats
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.template import Library

register = Library()


@register.inclusion_tag('admin/date_hierarchy.html')
def encounter_date_hierarchy(cl):
    """
    Date hierarchy tag for client encounter dates.

    Slightly adapted date_hierarchy template tag from
    django/contrib/admin/templatetags/admin_list.py.

    """
    dates_or_datetimes = 'dates' # TODO

    # For now, the field name is hardcoded - can be coverted to a parameter
    # of this tag if a generalization can be made to work.
    field_name = 'encounters__performed_on'

    year_field = '%s__year' % field_name
    month_field = '%s__month' % field_name
    day_field = '%s__day' % field_name
    field_generic = '_%s__' % field_name # Use the '_' prefix to bypass validations tied to valid field names.
    year_lookup = cl.params.get('_' + year_field)
    month_lookup = cl.params.get('_' + month_field)
    day_lookup = cl.params.get('_' + day_field)

    link = lambda filters: cl.get_query_string(filters, [field_generic])

    if not (year_lookup or month_lookup or day_lookup):
        # select appropriate start level
        date_range = cl.queryset.aggregate(first=models.Min(field_name),
                                            last=models.Max(field_name))
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
                'link': link({'_' + year_field: year_lookup, '_' + month_field: month_lookup}),
                'title': capfirst(formats.date_format(day, 'YEAR_MONTH_FORMAT'))
            },
            'choices': [{'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))}]
        }
    elif year_lookup and month_lookup:
        days = cl.queryset.filter(**{year_field: year_lookup, month_field: month_lookup})
        days = filter(bool, getattr(days, dates_or_datetimes)(field_name, 'day'))
        return {
            'show': True,
            'back': {
                'link': link({'_' + year_field: year_lookup}),
                'title': str(year_lookup)
            },
            'choices': [{
                'link': link({'_' + year_field: year_lookup, '_' + month_field: month_lookup, '_' + day_field: day.day}),
                'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))
            } for day in days]
        }
    elif year_lookup:
        months = cl.queryset.filter(**{year_field: year_lookup})
        months = filter(bool, getattr(months, dates_or_datetimes)(field_name, 'month'))
        return {
            'show': True,
            'back': {
                'link': link({}),
                'title': _('All dates')
            },
            'choices': [{
                'link': link({'_' + year_field: year_lookup, '_' + month_field: month.month}),
                'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
            } for month in months]
        }
    else:
        years = filter(bool, getattr(cl.queryset, dates_or_datetimes)(field_name, 'year'))
        return {
            'show': True,
            'choices': [{
                'link': link({'_' + year_field: str(year.year)}),
                'title': str(year.year),
            } for year in years]
        }
