# -*- coding: utf-8 -*-

'''
Created on 3.12.2011

@author: xaralis
'''
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
from django.utils.translation import ugettext_lazy as _

from boris.clients.models import Town, Person
from boris.services.models import Encounter
from boris.utils.widgets import SelectYearWidget


OUTPUT_BROWSER = 'browser'
OUTPUT_OFFICE = 'office'
OUTPUT_TYPES = (
    (OUTPUT_BROWSER, u'V prohlížeči'),
    (OUTPUT_OFFICE, 'Do souboru'),
)
class ReportForm(forms.Form):
    display = forms.ChoiceField(label=_(u'Zobrazit'), choices=OUTPUT_TYPES)


class MonthlyStatsForm(ReportForm):
    year = forms.IntegerField(widget=SelectYearWidget(history=10), label=_(u'Rok'))


class ServiceForm(ReportForm):
    date_from = forms.DateField(label=_(u'Od'), required=False, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=False, widget=AdminDateWidget())
    town = forms.ModelChoiceField(label=_(u'Město'),
                                  queryset=Town.objects.all(), required=False)
    person = forms.ModelChoiceField(label=_(u'Osoba'),
        queryset=Person.objects.all(), required=False,
        widget=ForeignKeyRawIdWidget(Encounter.person.field.rel))
