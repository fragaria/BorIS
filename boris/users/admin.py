'''
Created on 24.3.2012

@author: xaralis
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from boris.users.forms import BorisUserCreationForm


class BorisUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_superuser', 'is_active')
    add_form = BorisUserCreationForm


admin.site.unregister(User)
admin.site.register(User, BorisUserAdmin)
