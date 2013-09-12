'''
Created on 3.12.2011

@author: xaralis
'''
from datetime import date

from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select


class SplitDateWidget(SelectDateWidget):
    """
    Extend to avoid passing attrs to formfield_overrides - because
    if we did, admin would work only when web servery is just refreshed,
    on second view, it would be wasted :(
    """
    def __init__(self, attrs=None, required=False):
        super(SplitDateWidget, self).__init__(
            attrs=attrs, required=required,
            years=reversed(range(date.today().year - 100,
                                 date.today().year + 1))
        )


class SelectYearWidget(Select):
    def __init__(self, history=100, attrs=None):
            r = range(date.today().year - history, date.today().year + 1)
            super(SelectYearWidget, self).__init__(
                attrs=attrs,
                choices=reversed(zip(r, r))
            )
