# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

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
        available_in_modules = ['k', ]

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
        available_in_modules = ['k', ]


class HygienicService(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Hygienický servis')
        verbose_name_plural = _(u'Hygienické servisy')

    class Options:
        codenumber = 102
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class ClothesWashing(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Praní prádla')
        verbose_name_plural = _(u'Praní prádla')

    class Options:
        codenumber = 103
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class InternetUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Použití internetu klientem')
        verbose_name_plural = _(u'Použití internetu klientem')

    class Options:
        codenumber = 104
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class WorkTherapy(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pracovní terapie (samospráva)')
        verbose_name_plural = _(u'Pracovní terapie (samospráva)')

    class Options:
        codenumber = 105
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class WorkTherapyMeeting(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Schůzka pracovní terapie (samosprávy)')
        verbose_name_plural = _(u'Schůzka pracovní terapie (samosprávy)')

    class Options:
        codenumber = 106
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class CommunityWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Obecně prospěšné práce')
        verbose_name_plural = _(u'Obecně prospěšné práce')

    class Options:
        codenumber = 107
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class ParentAdvisory(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Poradenství pro rodiče')
        verbose_name_plural = _(u'Poradenství pro rodiče')

    class Options:
        codenumber = 108
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class PostUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pošta')
        verbose_name_plural = _(u'Pošty')

    class Options:
        codenumber = 109
        limited_to = ('Client', )
        available_in_modules = ['k', ]


class SocialServicesAgreement(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Uzavření dohody o poskytování sociálních služeb')  # The verbose_name of service is longer than 39 characters
        verbose_name_plural = _(u'Uzavření dohod o poskytování sociálních služeb')

    class Options:
        codenumber = 110
        limited_to = ('Client', )
        available_in_modules = ['k', ]

