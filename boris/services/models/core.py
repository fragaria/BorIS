# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from datetime import date
import operator

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_unicode
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager
from model_utils.models import TimeStampedModel

from fragapy.common.models.adminlink import AdminLinkMixin

from boris.services.forms import serviceform_factory


class ProxyInheritanceManager(InheritanceManager):
    """
    Filters proxy model's queryset by ContentType.

    Assumes its proxy models have ForeignKey to ContentType called
    'content_type'.
    """
    def get_query_set(self):
        qset = super(ProxyInheritanceManager, self).get_query_set()
        meta = self.model._meta
        if meta.proxy:
            content_type = ContentType.objects.get_by_natural_key(meta.app_label,
                meta.object_name.lower())
            return qset.filter(content_type=content_type)
        return qset


class EncounterManager(models.Manager):
    def first(self, year, towns=None):
        """Return the first encounters in the given year (and towns)."""
        date_start = date(year=year, month=1, day=1)
        date_stop = date(year=year, month=12, day=31)
        criteria = {'performed_on__gte': date_start, 'performed_on__lte': date_stop}
        if towns is not None:
            criteria.update({'where__in': towns})
        f_ects = self.filter(**criteria).values('person').annotate(min_date=models.Min('performed_on'))
        if not f_ects: # There are no encounters fulfilling the requirements.
            return self.filter(pk=-3)
        filters = reduce(operator.or_, [models.Q(person=e['person'], performed_on=e['min_date']) for e in f_ects])
        if towns is not None:
            return self.filter(filters).filter(where__in=towns)
        else:
            return self.filter(filters)


class Encounter(models.Model, AdminLinkMixin):
    person = models.ForeignKey('clients.Person', related_name='encounters',
        verbose_name=_(u'Osoba'))
    performed_by = models.ManyToManyField('auth.User', verbose_name=_(u'Kdo'))
    performed_on = models.DateField(default=date.today, verbose_name=_(u'Kdy'))
    where = models.ForeignKey('clients.Town', verbose_name=_(u'Kde'))
    is_by_phone = models.BooleanField(default=False, verbose_name=_(
        u'Telefonický kontakt'))

    objects = EncounterManager()

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
        self.codenumber = 0  # Code number to be displayed in the forms.
        self.include_in_reports = True

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

        ========================== ============================================
        Attribute                  Description
        ========================== ============================================
        ``title``                  Title used in forms and when saving.
                                   Defaults to verbose_name in Meta

        ``codenumber``             Code number used in forms, users are used
                                   to it.

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

        ``include_in_reports``     If set to True, the Service is included in the
                                   service reports. It's get_stats method is used
                                   to generate the statistics of interest.

        ========================== ============================================
    """
    __metaclass__ = ServiceMetaclass

    encounter = models.ForeignKey(Encounter, related_name='services',
        verbose_name=_(u'Kontakt'))
    title = models.CharField(max_length=255, editable=False,
        verbose_name=_(u'Název'))
    content_type = models.ForeignKey(ContentType, editable=False)

    objects = ProxyInheritanceManager()

    class Meta:
        app_label = 'services'
        ordering = ('encounter',)

    class Options:
        is_available = lambda person: False
        include_in_reports = False

    def __unicode__(self):
        return self.title

    def _prepare_title(self):
        return self.service.title

    @classmethod
    def real_content_type(cls):
        # @attention: instead of using get_for_model which doesn't respect
        # proxy models content types, use get_by_natural key as a workaround
        return ContentType.objects.get_by_natural_key(cls._meta.app_label,
                                                      cls._meta.object_name.lower())

    def clean(self):
        super(Service, self).clean()
        self.title = force_unicode(self._prepare_title())
        self.content_type = self.real_content_type()

    def cast(self):
        """
        When dealing with subclass that has been selected from base table,
        this will return the corresponding subclass instance.
        """
        try:
            return self.content_type.get_object_for_this_type(pk=self.pk)
        except ContentType.DoesNotExist:  # E.g mock. objects or some not-yet-saved objects.
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

    @classmethod
    def get_stats(cls, filtering):
        """
        Return an iterator over statisitics used in service reports.

        Returns an iterable over pairs of (<title>, <number>).
        """
        return (cls, cls._get_stats(filtering),)

    @classmethod
    def _get_stats(cls, filtering):
        title = cls.service.title
        cnt = cls.objects.filter(**filtering).count()
        return ((title, cnt),)


def service_list(person=None):
    """
    Returns a list of person's services registered in application.

    When `person` parameter is used, only those that can be provided
    to `person` will be listed.
    """
    if person:
        services = (
            s for s in Service.registered_services if s.service.is_available(person)
        )
    else:
        services = Service.registered_services
    return sorted(services, key=lambda x: x.service.codenumber)


def get_model_for_class_name(class_name):
    """Returns Service model class for given name"""
    for s in Service.registered_services:
        if s.__name__ == class_name:
            return s
    raise ValueError('Service `%s` is not registered' % class_name)
