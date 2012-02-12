'''
Created on 12.2.2012

@author: xaralis

Only used to provide needed patches to Django in-built models and stuff.
Called ``models.py`` so that the Django will import this.
'''
from django.contrib.auth.models import User

# add autocomplete fields list to django User to be able to use grappelli
# autocomplete lookup
User.autocomplete_search_fields = staticmethod(lambda : ('username__istartswith',))
