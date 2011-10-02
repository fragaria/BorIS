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
        
    def __init__(self, client, *args, **kwargs):
        if kwargs.has_key('initial'):
            kwargs['initial']['client'] = client
        else:
            kwargs['initial'] = {'client': client}
            
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.client = client
        
        self.fields['client'].widget = HiddenInput()