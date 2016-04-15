# -*- coding: utf-8 -*-
from itertools import chain

from django.db import models
from django.utils.translation import ugettext_lazy as _

from boris.services.models.basic import _boolean_stats
from .core import Service


def _group_service_title(instance, service):
    return service._meta.verbose_name + ' (%s): %s' % (instance.type.title, instance.name)


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
    def _get_stats(cls, filtering):
        from boris.clients.models import GroupContactType
        types = GroupContactType.objects.all()
        value_stats = []
        for _type in types:
            value_stats += _group_counselling_stats(cls, filtering, _type)
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
    def _get_stats(cls, filtering):
        boolean_stats = _boolean_stats(cls, filtering, ('clothing_wash', 'shower', 'social_clothing'))
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
        verbose_name = _(u'Pošta')
        verbose_name_plural = _(u'Pošty')

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


class PregnancyTest(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Těhotenský test')
        verbose_name_plural = _(u'Těhotenský test')

    class Options:
        codenumber = 25
        limited_to = ('Client', )


class Breathalyzer(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Alkotester')
        verbose_name_plural = _(u'Alkotester')

    class Options:
        codenumber = 26
        limited_to = ('Client', )