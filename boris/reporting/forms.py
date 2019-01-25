# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from boris.clients.models import Town, Person
from boris.services.models import Encounter, Service, service_list
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
    towns = forms.ModelMultipleChoiceField(label=_(u'Místo poskytnutí služby'), queryset=Town.objects.all(), required=False)


class ResidenceReportForm(BaseReportForm):
    towns_residence = forms.ModelMultipleChoiceField(label=_(u'Bydliště klienta'), queryset=Town.objects.all(), required=False)


class ServicesReportForm(ResidenceReportForm):
    def __init__(self, *args, **kwargs):
        super(ServicesReportForm, self).__init__(*args, **kwargs)
        # Remove services excluded from reporting
        unavailable_services = [service_model for service_model in service_list() if not service_model.service.include_in_reports]
        services_qset = ContentType.objects \
            .filter(app_label='services') \
            .exclude(model__in=[
                'service',
                'timedotation',
                'encounter',
            ] + [s._meta.object_name.lower() for s in unavailable_services])

        self.fields['services'] = forms.ModelMultipleChoiceField(label=_(u'Výkony'), required=False, queryset=services_qset)


class ClientsForm(ServicesReportForm):
    age_from = forms.IntegerField(label=_(u'Věk od'), required=False)
    age_to = forms.IntegerField(label=_(u'Věk do'), required=False)

    def clean(self):
        super(ClientsForm, self).clean()
        if self.cleaned_data['age_to'] is not None and self.cleaned_data['age_from'] is not None and \
           self.cleaned_data['age_to'] < self.cleaned_data['age_from']:
            raise ValidationError(_(u'Opravte prosím rozsah věku (do je menší než od).'))

    def clean_age_to(self):
        if self.cleaned_data['age_to'] is not None and self.cleaned_data['age_to'] < 0:
            raise ValidationError(_(u'Věk nemůže být záporný.'))
        return self.cleaned_data['age_to']

    def clean_age_from(self):
        if self.cleaned_data['age_from'] is not None and self.cleaned_data['age_from'] < 0:
            raise ValidationError(_(u'Věk nemůže být záporný.'))
        return self.cleaned_data['age_from']


class MonthlyStatsForm(ReportForm):
    year = forms.IntegerField(widget=SelectYearWidget(history=10), label=_(u'Rok'))


class ServiceForm(ResidenceReportForm):
    person = forms.ModelChoiceField(label=_(u'Osoba'),
        queryset=Person.objects.all(), required=False,
        widget=ForeignKeyRawIdWidget(Encounter.person.field.rel, admin.site))


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

class GovCouncilForm(ReportForm):
    date_from = forms.DateField(label=_(u'Od'), required=True, widget=AdminDateWidget())
    date_to = forms.DateField(label=_(u'Do'), required=True, widget=AdminDateWidget())
    kind = forms.ChoiceField(((1, u'Klienti'), (2, u'Výkony')),
                             label=_(u'Druh výstupu'), widget=forms.RadioSelect,
                             initial=1)
    towns = forms.ModelMultipleChoiceField(label=_(u'Město'),
                                           queryset=Town.objects.all(),
                                           required=False)
