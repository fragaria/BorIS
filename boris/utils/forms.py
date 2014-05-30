'''
Created on 2.10.2011

@author: xaralis
'''
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.db import models


def adminform_formfield(db_field, **kwargs):
    """
    Enables admin form widgets when used as formfield_callback.
    Use with CAUTION as using admin widgets is at your risk :)
    """
    if db_field.choices:
        return db_field.formfield(**kwargs)

    if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
        if isinstance(db_field, models.ForeignKey):
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel, admin.site)

        elif isinstance(db_field, models.ManyToManyField):
            kwargs['widget'] = widgets.ManyToManyRawIdWidget(db_field.rel, admin.site)
        formfield = db_field.formfield(**kwargs)

        if formfield:
#            related_modeladmin = admin.site._registry.get(db_field.rel.to)
#            can_add_related = bool(related_modeladmin and
#                            related_modeladmin.has_add_permission(request))
            formfield.widget = widgets.RelatedFieldWidgetWrapper(
                        formfield.widget, db_field.rel, admin.site,
                        can_add_related=True)

    for klass in db_field.__class__.mro():
        if klass in FORMFIELD_FOR_DBFIELD_DEFAULTS:
            kwargs = dict(FORMFIELD_FOR_DBFIELD_DEFAULTS[klass], **kwargs)
            return db_field.formfield(**kwargs)

    return db_field.formfield(**kwargs)
