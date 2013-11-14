# -*- coding: utf-8 -*-
from datetime import date

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
    def __init__(self, *args, **kwargs):
        super(HygieneForm, self).__init__(*args, **kwargs)
        current_year = date.today().year
        choices = list((('%s/%s' % (q, y), '%s/%s' % (q, y))
                       for y in reversed(range(current_year - 10, current_year + 1))
                       for q in reversed(range(1, 5))))

        self.fields['quarter'] = forms.ChoiceField(choices=choices, label=_(u'Období'))
        self.fields['towns'] = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                  queryset=Town.objects.all())
