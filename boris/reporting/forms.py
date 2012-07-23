# -*- coding: utf-8 -*-

'''
Created on 3.12.2011

@author: xaralis
'''
from django import forms
from django.utils.translation import ugettext_lazy as _

from boris.clients.models import Town, Person
from boris.utils.widgets import SelectYearWidget
from django.contrib.admin.widgets import AdminDateWidget


class MonthlyStatsForm(forms.Form):
    year = forms.IntegerField(widget=SelectYearWidget(history=10), label=_(u'Rok'))


class ServiceForm(forms.Form):
    date_from = forms.DateField(label=_(u'Od'), required=False, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=False, widget=AdminDateWidget())
    town = forms.ModelChoiceField(label=_(u'Město'),
                                  queryset=Town.objects.all(), required=False)
    person = forms.ModelChoiceField(label=_(u'Zaměstnanec'),
                                    queryset=Person.objects.all(),
                                    required=False)
