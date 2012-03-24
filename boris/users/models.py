'''
Created on 24.3.2012

@author: xaralis

Patch django.contrib.auth.models.User class with custom attributes.

'''
from django.contrib.auth.models import User

# add autocomplete fields list to django User to be able to use grappelli
# autocomplete lookup
User.autocomplete_search_fields = staticmethod(lambda: ('username__istartswith',))
