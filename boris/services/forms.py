'''
Created on 2.10.2011

@author: xaralis
'''
from django import forms
from django.forms.widgets import HiddenInput

class ServiceForm(forms.ModelForm):
    @property
    def template_list(self):
        return (
            'services/forms/%s.html' % self._meta.model.__name__.lower(),
            'services/forms/default.html'
        )
        
    def __init__(self, encounter, *args, **kwargs):
        if kwargs.has_key('initial'):
            kwargs['initial']['encounter'] = encounter
        else:
            kwargs['initial'] = {'encounter': encounter}
            
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.encounter = encounter
        
        self.fields['encounter'].widget = HiddenInput()