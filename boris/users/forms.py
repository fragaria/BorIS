'''
Created on 24.3.2012

@author: xaralis
'''
from django.contrib.auth.forms import UserCreationForm


class BorisUserCreationForm(UserCreationForm):
    """
    Set administration access to always ``True`` since whole app is based 
    on administration, right?
    """
    def save(self, commit=True):
        self.instance.is_staff = True
        return super(BorisUserCreationForm, self).save(commit)
