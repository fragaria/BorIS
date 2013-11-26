# -*- coding: utf-8 -*-
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
    (OUTPUT_OFFICE, u'Do souboru'),
)


class ReportForm(forms.Form):
    display = forms.ChoiceField(label=_(u'Zobrazit'), choices=OUTPUT_TYPES)


class BaseReportForm(ReportForm):
    date_from = forms.DateField(label=_(u'Od'), required=False, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=False, widget=AdminDateWidget())
    towns = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                  queryset=Town.objects.all(), required=False)

class MonthlyStatsForm(ReportForm):
    year = forms.IntegerField(widget=SelectYearWidget(history=10), label=_(u'Rok'))


class ServiceForm(ReportForm):
    date_from = forms.DateField(label=_(u'Od'), required=False, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=False, widget=AdminDateWidget())
    towns = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                           queryset=Town.objects.all(),
                                           required=False)
    person = forms.ModelChoiceField(label=_(u'Osoba'),
        queryset=Person.objects.all(), required=False,
        widget=ForeignKeyRawIdWidget(Encounter.person.field.rel))


class HygieneForm(ReportForm):
    display = forms.ChoiceField(label=_(u'Zobrazit'), choices=OUTPUT_TYPES,
                                initial=OUTPUT_BROWSER, widget=forms.HiddenInput)
    date_from = forms.DateField(label=_(u'Od'), required=True, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=True, widget=AdminDateWidget())
    kind = forms.ChoiceField(((1, u'Prevalence'), (2, u'Incidence')),
                             label=_(u'Druh výstupu'), widget=forms.RadioSelect,
                             initial=1)
    towns = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                           queryset=Town.objects.all(),
                                           required=False)
