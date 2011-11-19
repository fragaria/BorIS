# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from boris.classification import DISEASES, DISEASE_TEST_SIGN

from .core import Service

class HarmReduction(Service):
    in_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'IN'))
    out_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'OUT'))

    sterilized_water = models.BooleanField(default=False,
        verbose_name=_(u'sterilizovaná voda'))
    cotton_filters = models.BooleanField(default=False,
        verbose_name=_(u'bavlněné filtry'))
    alcohol_swabs = models.BooleanField(default=False,
        verbose_name=_(u'alkoholové tampony'))
    acid = models.BooleanField(default=False, verbose_name=_(u'kyselina'))
    alu_foil = models.BooleanField(default=False, verbose_name=_(u'alobal'))
    condoms = models.BooleanField(default=False, verbose_name=_(u'kondomy'))
    jelly_capsules = models.BooleanField(default=False,
        verbose_name=_(u'želatinové kapsle'))
    stericup = models.BooleanField(default=False, verbose_name=_(u'stéricup'))
    other = models.BooleanField(default=False, verbose_name=_(u'jiné'))

    pregnancy_test = models.BooleanField(default=False, verbose_name=_(u'těhotenský test'))
    medical_supplies = models.BooleanField(default=False, verbose_name=_(
        u'zdravotnický materiál'), help_text=_(u'náplasti, buničina, vitamíny, '
        '...'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Harm Reduction')
        verbose_name_plural = _(u'Harm Reduction')

    class Options:
        title = _(u'Výměnný a jiný harm reduction program')
        form_template = 'services/forms/small_cells.html'
        fieldsets = (
            (None, {'fields': ('in_count', 'out_count', 'encounter'),
                'classes': ('inline',)}),
            (_(u'Harm Reduction'), {'fields': (
                'sterilized_water', 'cotton_filters', 'alcohol_swabs', 'acid',
                'alu_foil', 'condoms', 'jelly_capsules', 'stericup', 'other',
            ), 'classes': ('inline',)}),
            (_(u'Ostatní'), {'fields': ('pregnancy_test', 'medical_supplies'),
                'classes': ('inline',)})
        )


class IncomeExamination(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Vstupní zhodnocení stavu klienta')
        verbose_name_plural = _(u'Vstupní zhodnocení stavu klienta')


class DiseaseTest(Service):
    disease = models.PositiveSmallIntegerField(choices=DISEASES,
        verbose_name=_(u'Testované onemocnění'))
    sign = models.CharField(max_length=1, choices=DISEASE_TEST_SIGN,
        default=DISEASE_TEST_SIGN.INCONCLUSIVE, verbose_name=_(u'Stav'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Testování infekčních nemocí')
        verbose_name_plural = _(u'Testování infekčních nemocí')

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
        form_template = 'services/forms/small_cells.html'
        fieldsets = (
            (None, {
                'fields': ('encounter', 'safe_usage', 'safe_sex', 'medical',
                    'socio_legal', 'cure_possibilities', 'literature', 'other'),
                'classes': ('inline',)
            }),
        )


class ContactWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Kontaktní práce')
        verbose_name_plural = _(u'Kontaktní práce')


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


class SocialWork(Service):
    socio_legal = models.BooleanField(default=False,
        verbose_name=_(u'sociálně-právní'))
    socio_material = models.BooleanField(default=False,
        verbose_name=_(u'sociálně-materiální'))
    service_mediation = models.BooleanField(default=False,
        verbose_name=_(u'zprostředkování dalších služeb'))
    other = models.BooleanField(default=False,
        verbose_name=_(u'jiná'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Sociální práce')
        verbose_name_plural = _(u'Sociální práce')

    class Options:
        fieldsets = (
            (None, {
                'fields': ('encounter', 'socio_legal', 'socio_material',
                    'service_mediation', 'other'),
                'classes': ('inline',)
            }),
        )


class UtilityWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Další úkony')
        verbose_name_plural = _(u'Další úkony')

    class Options:
        title = _(u'Úkony potřebné pro zajištění práce s klientem')


class BasicMedicalTreatment(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Základní zdravotní ošetření')
        verbose_name_plural = _(u'Základní zdravotní ošetření')


class IndividualCounseling(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Individuální poradenství')
        verbose_name_plural = _(u'Individuální poradenství')


