# -*- coding: utf-8 -*-
from itertools import chain

from django.db import models
from django.utils.translation import ugettext_lazy as _

from boris.services.models.basic import _boolean_stats
from .core import Service


def _group_service_title(instance, service):
    return service._meta.verbose_name + ' (%s)' % instance.type.title


def _group_counselling_stats(model, filtering, _type):
    """Get stats for choice fields for any service class."""
    stats = []
    filtering_bln = {'encounter__group_contact__type__key': _type.key}
    filtering_bln.update(filtering)
    cnt = model.objects.filter(**filtering_bln).values_list('encounter__group_contact__pk', flat=True).distinct().count()
    stats.append((_type, cnt))
    return stats


class GroupCounselling(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Skupinové poradenství')
        verbose_name_plural = _(u'Skupinová poradenství')

    class Options:
        codenumber = 15
        limited_to = ('Client', )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False, only_basic=False):
        from boris.clients.models import GroupContactType
        types = GroupContactType.objects.all()
        value_stats = []
        for _type in types:
            value_stats += _group_counselling_stats(cls, filtering, _type)
        if only_subservices:
            return chain(value_stats)
        return chain(  # The total count is computed differently than usually.
            ((cls.service.title, sum(stat[1] for stat in value_stats)),),
            value_stats,
        )


class ContactRoom(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Kontaktní místnost')
        verbose_name_plural = _(u'Kontaktní místnosti')

    class Options:
        codenumber = 16
        limited_to = ('Client', )


class HygienicService(Service):
    clothing_wash = models.BooleanField(default=False,
                                     verbose_name=_(u'1) praní prádla'))
    shower = models.BooleanField(default=False,
                                     verbose_name=_(u'2) sprcha'))
    social_clothing = models.BooleanField(default=False,
                                     verbose_name=_(u'3) sociální šatník'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Hygienický servis')
        verbose_name_plural = _(u'Hygienické servisy')

    class Options:
        codenumber = 17
        form_template = 'services/forms/small_cells.html'
        limited_to = ('Client', )
        fieldsets = (
            (None, {
                'fields': ('encounter', 'clothing_wash', 'shower', 'social_clothing'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False, only_basic=False):
        boolean_stats = _boolean_stats(cls, filtering, ('clothing_wash', 'shower', 'social_clothing'))
        if only_subservices:
            return chain(boolean_stats)
        return chain( # The total count is computed differently than usually.
                ((cls.service.title, sum(stat[1] for stat in boolean_stats)),),
                boolean_stats,
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False, only_basic=False):
        boolean_stats = _boolean_stats(cls, filtering, ('clothing_wash', 'shower', 'social_clothing'))
        if only_subservices:
            return chain(boolean_stats)
        return chain( # The total count is computed differently than usually.
                ((cls.service.title, sum(stat[1] for stat in boolean_stats)),),
                boolean_stats,
        )


class InternetUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Použití internetu klientem')
        verbose_name_plural = _(u'Použití internetu klientem')

    class Options:
        codenumber = 18
        limited_to = ('Client', )


class WorkTherapy(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pracovní terapie (samospráva)')
        verbose_name_plural = _(u'Pracovní terapie (samospráva)')

    class Options:
        codenumber = 19
        limited_to = ('Client', )


class WorkTherapyMeeting(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Schůzka pracovní terapie (samosprávy)')
        verbose_name_plural = _(u'Schůzka pracovní terapie (samosprávy)')

    class Options:
        codenumber = 20
        limited_to = ('Client', )


class CommunityWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Obecně prospěšné práce')
        verbose_name_plural = _(u'Obecně prospěšné práce')

    class Options:
        codenumber = 21
        limited_to = ('Client', )


class PostUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Korespondenční práce')
        verbose_name_plural = _(u'Korespondenční práce')

    class Options:
        codenumber = 22
        limited_to = ('Client', )


class SocialServicesAgreement(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Uzavření dohody o poskyt. soc. služeb')
        verbose_name_plural = _(u'Uzavření dohod o poskyt. soc. služeb')

    class Options:
        codenumber = 23
        limited_to = ('Client', )


class FoodService(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Potravinový servis')
        verbose_name_plural = _(u'Potravinový servis')

    class Options:
        codenumber = 24
        limited_to = ('Client', )


class UrineTest(Service):
    drug_test = models.BooleanField(default=False,
                                    verbose_name=_(u'a) Test na drogy'))
    pregnancy_test = models.BooleanField(default=False,
                                         verbose_name=_(u'b) Těhotenský test'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Orientační test z moči')
        verbose_name_plural = _(u'Orientační test z moči')

    class Options:
        codenumber = 25
        limited_to = ('Client', )
        fieldsets = (
            (None, {
                'fields': ('encounter', 'drug_test', 'pregnancy_test'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False, only_basic=False):
        boolean_stats = _boolean_stats(cls, filtering, ('drug_test', 'pregnancy_test'))
        if only_subservices:
            return chain(boolean_stats)
        return chain( # The total count is computed differently than usually.
                ((cls.service.title, sum(stat[1] for stat in boolean_stats)),),
                boolean_stats,
        )


class Breathalyzer(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Alkotester')
        verbose_name_plural = _(u'Alkotester')

    class Options:
        codenumber = 26
        limited_to = ('Client', )


class WorkWithFamily(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Práce s rodinou')
        verbose_name_plural = _(u'Práce s rodinami')

    class Options:
        codenumber = 27
        limited_to = ('Client', )