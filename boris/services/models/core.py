# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager

from fragapy.common.models.adminlink import AdminLinkMixin

from boris.services.forms import serviceform_factory
from django.utils.functional import curry

class Encounter(models.Model, AdminLinkMixin):
    person = models.ForeignKey('clients.Person', related_name='encounters',
        verbose_name=_(u'Osoba'))
    performed_by = models.ManyToManyField('auth.User', verbose_name=_(u'Kdo'))
    performed_on = models.DateField(default=date.today, verbose_name=_(u'Kdy'))
    where = models.ForeignKey('clients.Town', verbose_name=_(u'Kde'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Kontakt')
        verbose_name_plural = _(u'Kontakty')
        ordering = ('-performed_on',)

    def service_count(self):
        return self.services.all().count()
    service_count.short_description = _(u'Počet výkonů')

    def __unicode__(self):
        return unicode(self.person)


class ServiceOptions(object):
    """
    This class is similar to `Options` class that Django defines for every model.

    It is used to keep settings for all Service subclasses.
    """
    def __init__(self, model):
        self.model = model
        self.title = ''
        self.description_template = None
        self.form_template = None
        self.limited_to = ()
        self.is_available = lambda person: False
        self.fields = None
        self.excludes = None
        self.row_attrs = None
        self.fieldsets = None

    def get_description_template_list(self):
        return (self.description_template, 'services/desc/default.html')

    def get_description(self):
        """
        Returns rendered description of this service (can contain HTML).
        """
        from django import template
        t = template.loader.select_template(self.get_description_template_list())
        return t.render(template.Context())

    def get_fieldsets(self):
        """
        Returns fieldsets to use when rendering the edit form.
        """
        if self.fieldsets:
            return self.fieldsets
        else:
            fields = [f.name for f in self.model._meta.fields if f.editable]
            return ((None, {'fields': fields}),)


class ServiceMetaclass(models.Model.__metaclass__):
    registered_services = []

    def __new__(cls, name, bases, attrs):
        new_cls = super(ServiceMetaclass, cls).__new__(cls, name, bases, attrs)

        if not new_cls._meta.abstract:
            cls.registered_services.append(new_cls)

        service_meta = {
            'title': new_cls._meta.verbose_name,
            'description_template': 'services/desc/%s.html' % name.lower(),
            'is_available': lambda person: not new_cls._meta.abstract,
        }
        attrs_service_meta = attrs.pop('Options', None)

        if attrs_service_meta:
            service_meta.update(attrs_service_meta.__dict__)

        def specific_person_passes_test(person_classes, func, person):
            if person.cast().__class__.__name__ in person_classes:
                return func(person)
            return False

        # If `limited_to` is supplied, transform the `is_available` function
        # so that if will eventually return True only when person given
        # as it's parameter is of type which name is listed in `limited_to`
        if 'limited_to' in service_meta:
            service_meta['is_available'] = curry(specific_person_passes_test,
                service_meta['limited_to'], service_meta['is_available'])

        new_cls.service = ServiceOptions(new_cls)
        new_cls.service.__dict__.update(service_meta)

        return new_cls


class Service(TimeStampedModel):
    """
    ``Service`` is a base model for defining services which workers did in
    some encounter with a person (e.g. a client).

    ``Service`` subclasses can state special ``Options`` nested class
    in similar fashion to a well-known `Meta` class that Django model can
    define.

    To register the class for editing in admin interface subclassing is
    the only thing you need.

    ``Options`` nested class can have following attributes to allow for
    customizations::

        ========================== =============================================
        Attribute                  Description
        ========================== =============================================
        ``title``                  Title used in forms and when saving.
                                   Defaults to verbose_name in Meta

        ``description_template``   Template path to use for service description
                                   rendering. Defaults to 'services/desc/default.html'

        ``form_template``          Template to use when rendering service form.
                                   Defaults to 'services/forms/default.html'

        ``is_available``           Function to use when deciding whether
                                   this service should be proposed for given
                                   person. Takes `person` argument.
                                   Defaults to 'not model._meta.abstract'.

        ``limited_to``             When supplied, before checking `is_available`,
                                   check for Person type, to which encounter
                                   is related is made. Iterable of class-names
                                   representing Person subtypes is expected, e.g.:
                                   limited_to = ('Client', 'Anonymous')

        ``row_attrs``              Row attrs as defined in BetterForm implentation.

        ``fieldsets``              Fieldsets to use when rendering the form.
                                   Defaults to one fieldset with no legend and
                                   all the fields.
        ========================== =============================================
    """
    __metaclass__ = ServiceMetaclass

    encounter = models.ForeignKey(Encounter, related_name='services',
        verbose_name=_(u'Kontakt'))
    title = models.CharField(max_length=255, editable=False,
        verbose_name=_(u'Název'))
    content_type = models.ForeignKey(ContentType, editable=False)

    objects = InheritanceManager()

    class Meta:
        app_label = 'services'
        ordering = ('encounter',)

    class Options:
        is_available = lambda person: False

    def __unicode__(self):
        return self.title

    def _prepare_title(self):
        return self.service.title

    def clean(self):
        super(Service, self).clean()
        self.title = force_unicode(self._prepare_title())
        # @attention: instead of using get_for_model which doesn't respect
        # proxy models content types, use get_by_natural key as a workaround
        self.content_type = ContentType.objects.get_by_natural_key(
            self._meta.app_label, self._meta.object_name.lower())

    def cast(self):
        """
        When dealing with subclass that has been selected from base table,
        this will return the corresponding subclass instance.
        """
        try:
            return self.content_type.get_object_for_this_type(pk=self.pk)
        except ContentType.DoesNotExist: # E.g mock. objects or some not-yet-saved objects.
            return self


    @classmethod
    def form(cls, *args, **kwargs):
        """
        Returns completely initialized form class for service editing.
        """
        return serviceform_factory(cls)

    def is_editable(self):
        """
        Returns True if this service is user-editable - if it has something
        what a user can change.
        """
        skip_fields = ('encounter', 'id', 'service_ptr')
        return any([f.editable for f in self._meta.fields if f.name not in skip_fields])

    @classmethod
    def class_name(cls):
        return cls.__name__


def service_list(person=None):
    """
    Returns tuple of person's services registered in application.

    When `person` parameter is used, only those that can be provided
    to `person` will be listed.
    """
    if person:
        return (s for s in Service.registered_services if s.service.is_available(person))
    return Service.registered_services


def get_model_for_class_name(class_name):
    """Returns Service model class for given name"""
    for s in Service.registered_services:
        if s.__name__ == class_name:
            return s
    raise ValueError('Service `%s` is not registered' % class_name)
