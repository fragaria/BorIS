'''
Created on 2.10.2011

@author: xaralis
'''
from form_utils.forms import BetterModelForm, BetterModelFormMetaclass

from django.forms.widgets import HiddenInput
from boris.utils.forms import adminform_formfield
from django.contrib.contenttypes.models import ContentType

# from boris.clients.models import Client, Town, Anamnesis, DrugUsage, \
#     RiskyManners, Region, District, DiseaseTest, Anonymous, \
#     PractitionerContact, Person, GroupContact, ClientCard, GroupContactType

# from boris.services.models.core import get_model_for_class_name, Service, \
#     Encounter


class ServiceForm(BetterModelForm):
    @property
    def template_list(self):
        if self._meta.model.service.form_template is not None:
            return (self._meta.model.service.form_template,)
        return (
            'services/forms/%s.html' % self._meta.model.__name__.lower(),
            'services/forms/default.html'
        )

    def __init__(self, encounter, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['encounter'] = encounter
        else:
            kwargs['initial'] = {'encounter': encounter}

        super(ServiceForm, self).__init__(*args, **kwargs)

        self.fields['encounter'].widget = HiddenInput()
        self.encounter = encounter


def serviceform_factory(model, form=ServiceForm, fields=None, excludes=None,
                        fieldsets=None, row_attrs=None,
                        formfield_callback=adminform_formfield):

    service = model.service

    if fields is None:
        fields = service.fields
    if excludes is None:
        excludes = service.excludes
    if fieldsets is None:
        fieldsets = service.get_fieldsets()
    if row_attrs is None:
        row_attrs = service.row_attrs

    attrs = {
        'model': model,
    }
    if fields is not None:
        attrs['fields'] = fields
    if excludes is not None:
        attrs['excludes'] = excludes
    if fieldsets is not None:
        attrs['fieldsets'] = fieldsets
    if row_attrs is not None:
        attrs['row_attrs'] = row_attrs

    Meta = type('Meta', (object,), attrs)

    class_name = model.__name__ + 'ServiceForm'

    form_class_attrs = {
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }

    return BetterModelFormMetaclass(class_name, (form,), form_class_attrs)
