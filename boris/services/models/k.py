# -*- coding: utf-8 -*-
from itertools import chain
from django.utils.translation import ugettext_lazy as _
from django.db import models
from boris.services.models.basic import _boolean_stats

from .core import Service


class GroupCounselling(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Skupinové poradenství')
        verbose_name_plural = _(u'Skupinová poradenství')

    class Options:
        codenumber = 100
        limited_to = ('Client', )

    @classmethod
    def get_stats(cls, filtering):
        return super(GroupCounselling, cls).get_stats(filtering)

    @classmethod
    def _get_stats(cls, filtering):
        return super(GroupCounselling, cls)._get_stats(filtering)


class ContactRoom(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Kontaktní místnost')
        verbose_name_plural = _(u'Kontaktní místnosti')

    class Options:
        codenumber = 101
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
        codenumber = 102
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
        codenumber = 103
        limited_to = ('Client', )


class WorkTherapy(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pracovní terapie (samospráva)')
        verbose_name_plural = _(u'Pracovní terapie (samospráva)')

    class Options:
        codenumber = 104
        limited_to = ('Client', )


class WorkTherapyMeeting(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Schůzka pracovní terapie (samosprávy)')
        verbose_name_plural = _(u'Schůzka pracovní terapie (samosprávy)')

    class Options:
        codenumber = 105
        limited_to = ('Client', )


class CommunityWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Obecně prospěšné práce')
        verbose_name_plural = _(u'Obecně prospěšné práce')

    class Options:
        codenumber = 106
        limited_to = ('Client', )


class PostUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pošta')
        verbose_name_plural = _(u'Pošty')

    class Options:
        codenumber = 108
        limited_to = ('Client', )


class SocialServicesAgreement(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Uzavření dohody o poskyt. soc. služeb')
        verbose_name_plural = _(u'Uzavření dohod o poskyt. soc. služeb')

    class Options:
        codenumber = 109
        limited_to = ('Client', )


class FoodService(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Potravinový servis')
        verbose_name_plural = _(u'Potravinový servis')

    class Options:
        codenumber = 110
        limited_to = ('Client', )


class PregnancyTest(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Těhotenský test')
        verbose_name_plural = _(u'Těhotenský test')

    class Options:
        codenumber = 111
        limited_to = ('Client', )


class Breathalyzer(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Alkotester')
        verbose_name_plural = _(u'Alkotester')

    class Options:
        codenumber = 112
        limited_to = ('Client', )