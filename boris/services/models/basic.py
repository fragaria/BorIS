# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from itertools import chain

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from boris.classification import DISEASES, DISEASE_TEST_SIGN

from .core import Service


def _boolean_stats(model, filtering, field_names):
    """Get stats for boolean fields for any service class."""
    boolean_stats = []
    for fname in field_names:
        title = model._meta.get_field(fname).verbose_name.__unicode__()
        filtering_bln = {fname: True}
        filtering_bln.update(filtering)
        cnt = model.objects.filter(**filtering_bln).count()
        boolean_stats.append((title, cnt))
    return boolean_stats


class HarmReduction(Service):
    in_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'IN'))
    out_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'OUT'))
    svip = models.PositiveIntegerField(blank=True, null=True,
        verbose_name=_(u'pro počet osob (SVIP)'))

    standard = models.BooleanField(default=False,
        verbose_name=_(u'standard'),
        help_text=_(u'sterilní voda, filtry, alkoholové tampony'))
    acid = models.BooleanField(default=False, verbose_name=_(u'kyselina'))
    alternatives = models.BooleanField(default=False,
            verbose_name=_(u'alternativy'),
            help_text=_(u'alobal, kapsle, šňupátka'))
    condoms = models.BooleanField(default=False, verbose_name=_(u'prezervativy'))
    stericup = models.BooleanField(default=False, verbose_name=_(u'Stéri-cup/filt'))
    other = models.BooleanField(default=False, verbose_name=_(u'jiný materiál'))

    pregnancy_test = models.BooleanField(default=False, verbose_name=_(u'těhotenský test'))
    medical_supplies = models.BooleanField(default=False, verbose_name=_(
        u'zdravotní'), help_text=_(u'masti, náplasti, buničina, vitamíny, škrtidlo'
        '...'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Harm Reduction')
        verbose_name_plural = _(u'Harm Reduction')

    class Options:
        codenumber = 3
        title = _(u'Výměnný a jiný harm reduction program')
        form_template = 'services/forms/small_cells.html'
        limited_to = ('Client',)
        fieldsets = (
            (None, {'fields': ('in_count', 'out_count', 'svip', 'encounter'),
                'classes': ('inline',)}),
            (_(u'Harm Reduction'), {'fields': (
                'standard', 'alternatives', 'acid',
                'condoms', 'stericup', 'other',
            ), 'classes': ('inline',)}),
            (_(u'Ostatní'), {'fields': ('pregnancy_test', 'medical_supplies'),
                'classes': ('inline',)})
        )

    def _prepare_title(self):
        return u'%s (%s / %s)' % (self.service.title,
                                  self.in_count,
                                  self.out_count)

    @classmethod
    def get_stats(cls, filtering):
        basic_stats = super(HarmReduction, cls).get_stats(filtering)
        booleans = ('standard', 'acid', 'alternatives', 'condoms', 'stericup',
            'other', 'pregnancy_test', 'medical_supplies')
        boolean_stats = _boolean_stats(cls, filtering, booleans)
        in_cnt = cls.objects.filter(**filtering).aggregate(Sum('in_count'))
        in_stats = ((_('IN total'), in_cnt['in_count__sum'] or 0),)
        out_cnt = cls.objects.filter(**filtering).aggregate(Sum('out_count'))
        out_stats = ((_('OUT total'), out_cnt['out_count__sum'] or 0),)
        return chain(basic_stats, boolean_stats, in_stats, out_stats)


class IncomeExamination(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'První kontakt')
        verbose_name_plural = _(u'První kontakty')

    class Options:
        codenumber = 1


class DiseaseTest(Service):
    disease = models.PositiveSmallIntegerField(choices=DISEASES,
        verbose_name=_(u'Testované onemocnění'))
    sign = models.CharField(max_length=1, choices=DISEASE_TEST_SIGN,
        default=DISEASE_TEST_SIGN.INCONCLUSIVE, verbose_name=_(u'Stav'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Testování infekčních nemocí')
        verbose_name_plural = _(u'Testování infekčních nemocí')

    class Options:
        codenumber = 8
        limited_to = ('Client',)

    def _prepare_title(self):
        return _(u'%(title)s: %(disease)s / %(sign)s') % {
            'title': self.service.title, 'disease': self.get_disease_display(),
            'sign': self.get_sign_display()
        }


class AsistService(Service):
    ASIST_TYPES = Choices(
        ('d', 'DOCTOR', _(u'lékař')),
        ('o', 'OFFICE', _(u'úřad')),
        ('m', 'MEDICAL_FACILITY', _(u'léčebné zařízení')),
    )
    where = models.CharField(max_length=1, choices=ASIST_TYPES, verbose_name=_(u'Kam'))
    note = models.TextField(null=True, blank=True, verbose_name=_(u'Poznámka'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Asistenční služba')
        verbose_name_plural = _(u'Asistenční služby')

    class Options:
        codenumber = 9
        limited_to = ('Client',)

    def _prepare_title(self):
        return _(u'%(title)s: doprovod %(where)s') % {
            'title': self.service.title, 'where': self.get_where_display()
        }


class InformationService(Service):
    safe_usage = models.BooleanField(default=False,
        verbose_name=_(u'bezpečné užívání'))
    safe_sex = models.BooleanField(default=False,
        verbose_name=_(u'bezpečný sex'))
    medical = models.BooleanField(default=False, verbose_name=_(u'zdravotní'))
    socio_legal = models.BooleanField(default=False,
        verbose_name=_(u'sociálně-právní'))
    cure_possibilities = models.BooleanField(default=False,
        verbose_name=_(u'možnosti léčby'))
    literature = models.BooleanField(default=False,
        verbose_name=_(u'literatura'))
    other = models.BooleanField(default=False, verbose_name=_(u'ostatní'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Informační servis')
        verbose_name_plural = _(u'Informační servis')

    class Options:
        codenumber = 10
        form_template = 'services/forms/small_cells.html'
        fieldsets = (
            (None, {
                'fields': ('encounter', 'safe_usage', 'safe_sex', 'medical',
                    'socio_legal', 'cure_possibilities', 'literature', 'other'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def get_stats(cls, filtering):
        basic_stats = super(InformationService, cls).get_stats(filtering)
        booleans = ('safe_usage', 'safe_sex', 'medical', 'socio_legal',
            'cure_possibilities', 'literature', 'other')
        boolean_stats = _boolean_stats(cls, filtering, booleans)
        return chain(basic_stats, boolean_stats)


class ContactWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Kontaktní práce')
        verbose_name_plural = _(u'Kontaktní práce')

    class Options:
        codenumber = 4

class CrisisIntervention(Service):
    INTERVENTION_TYPES = Choices(
        ('d', 'DIRECT', _(u'přímá')),
        ('p', 'OVER_THE_PHONE', _(u'po telefonu')),
    )
    type = models.CharField(max_length=1, choices=INTERVENTION_TYPES,
        default=INTERVENTION_TYPES.DIRECT, verbose_name=_(u'Typ'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Krizová intervence')
        verbose_name_plural = _(u'Krizové intervence')

    class Options:
        codenumber = 7
        limited_to = ('Client',)

    def _prepare_title(self):
        return _(u'%(title)s: %(type)s') % {
            'title': self.service.title, 'type': self.get_type_display()
        }


class PhoneCounseling(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Telefonické poradenství')
        verbose_name_plural = _(u'Telefonické poradenství')

    class Options:
        codenumber = 11


class SocialWork(Service):
    socio_legal = models.BooleanField(default=False,
        verbose_name=_(u'sociálně-právní'))
    counselling = models.BooleanField(default=False,
        verbose_name=_(u'předléčebné indiviuální poradenství'))
    service_mediation = models.BooleanField(default=False,
        verbose_name=_(u'zprostředkování dalších služeb'))
    other = models.BooleanField(default=False,
        verbose_name=_(u'jiná'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Sociální práce')
        verbose_name_plural = _(u'Sociální práce')

    class Options:
        codenumber = 6
        limited_to = ('Client',)
        fieldsets = (
            (None, {
                'fields': ('encounter', 'socio_legal', 'counselling',
                    'service_mediation', 'other'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def get_stats(cls, filtering):
        basic_stats = super(SocialWork, cls).get_stats(filtering)
        booleans = ('socio_legal', 'counselling', 'service_mediation', 'other')
        boolean_stats = _boolean_stats(cls, filtering, booleans)
        return chain(basic_stats, boolean_stats)


class UtilityWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Odkazy a zprostředkování')
        verbose_name_plural = _(u'Odkazy a zprostředkování')

    class Options:
        codenumber = 12
        limited_to = ('Client',)


class BasicMedicalTreatment(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Základní zdravotní ošetření')
        verbose_name_plural = _(u'Základní zdravotní ošetření')

    class Options:
        codenumber = 13
        limited_to = ('Client',)


class IndividualCounseling(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Základní poradenství')
        verbose_name_plural = _(u'Základní poradenství')

    class Options:
        codenumber = 5
        limited_to = ('Client',)


class Address(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Oslovení')
        verbose_name_plural = _(u'Oslovení')

    class Options:
        codenumber = 2
