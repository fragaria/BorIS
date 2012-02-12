'''
Created on 3.12.2011

@author: xaralis
'''
from django import forms
from django.utils.translation import ugettext_lazy as _

from boris.utils.widgets import SelectYearWidget

class MonthlyStatsForm(forms.Form):
    year = forms.IntegerField(widget=SelectYearWidget(history=10), label=_(u'Rok'))
