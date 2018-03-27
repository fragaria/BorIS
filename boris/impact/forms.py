# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
from django.utils.translation import ugettext_lazy as _

from boris.clients.models import Town, Person
from boris.reporting.forms import ReportForm


class ImpactForm(ReportForm):
    date_from = forms.DateField(label=_(u'Od'), required=True, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=True, widget=AdminDateWidget())
    towns = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                           queryset=Town.objects.all(),
                                           required=False)

