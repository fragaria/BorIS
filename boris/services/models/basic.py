# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from collections import defaultdict
from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, Max, Avg
from django.utils.translation import ugettext_lazy as _, ugettext

from model_utils import Choices

from fragapy.fields.models import MultiSelectField

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
    return tuple(boolean_stats)


def _field_label(model, field):
    return model._meta.get_field(field).verbose_name.__unicode__()


def _sum_int(model, filtering, field):
    return model.objects.filter(**filtering).aggregate(Sum(field))['%s__sum' % field] or 0


def _max_int(model, filtering, field):
    return model.objects.filter(**filtering).aggregate(Max(field))['%s__max' % field] or 0


def _avg_int(model, filtering, field):
    return model.objects.filter(**filtering).aggregate(Avg(field))['%s__avg' % field] or 0



class HarmReduction(Service):
    in_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'IN'))
    out_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'OUT'))
    svip_person_count = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'počet osob ve SVIP'))

    standard = models.BooleanField(default=False,
        verbose_name=_(u'1) standard'),
        help_text=_(u'sterilní voda, filtry, alkoholové tampony'))
    acid = models.BooleanField(default=False, verbose_name=_(u'3) kyselina'))
    alternatives = models.BooleanField(default=False,
            verbose_name=_(u'2) alternativy'),
            help_text=_(u'alobal, kapsle, šňupátka'))
    condoms = models.BooleanField(default=False, verbose_name=_(u'4) prezervativy'))
    stericup = models.BooleanField(default=False, verbose_name=_(u'5) Stéri-cup/filt'))
    other = models.BooleanField(default=False, verbose_name=_(u'6) jiný materiál'))

    pregnancy_test = models.BooleanField(default=False, verbose_name=_(u'7) těhotenský test'))
    medical_supplies = models.BooleanField(default=False, verbose_name=_(
        u'8) zdravotní'), help_text=_(u'masti, náplasti, buničina, vitamíny, škrtidlo'
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
            (None, {'fields': ('in_count', 'out_count', 'svip_person_count',
                               'encounter'),
                    'classes': ('inline',)}),
            (_(u'Harm Reduction'), {'fields': ('standard', 'alternatives',
                                               'acid', 'condoms', 'stericup',
                                               'other'),
                                    'classes': ('inline',)}),
            (_(u'Ostatní'), {'fields': ('pregnancy_test', 'medical_supplies'),
                             'classes': ('inline',)})
        )

    def _prepare_title(self):
        return u'%s (%s / %s)' % (self.service.title,
                                       self.in_count,
                                       self.out_count)

    @classmethod
    def _get_stats(cls, filtering):
        return chain(
            super(HarmReduction, cls)._get_stats(filtering),
            _boolean_stats(cls, filtering, ('standard', 'alternatives',
                                            'acid', 'condoms',
                                            'stericup', 'other',
                                            'pregnancy_test',
                                            'medical_supplies')),
            ((_field_label(cls, 'in_count'), _sum_int(cls, filtering, 'in_count')),),
            ((_field_label(cls, 'out_count'), _sum_int(cls, filtering, 'out_count')),),
            ((_(u'Průměrný počet osob ve SVIP'), int(round(_avg_int(cls, filtering,
                'svip_person_count')))),),
            ((_(u'Nejvyšší počet osob ve SVIP'), _max_int(cls, filtering,
                'svip_person_count')),),
        )


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
        default=DISEASES.HIV, verbose_name=_(u'Testované onemocnění'))
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
        return _(u'%(title)s: %(disease)s') % {
            'title': self.service.title, 'disease': self.get_disease_display()
        }

class AsistService(Service):
    ASIST_TYPES = Choices(
        ('m', 'MEDICAL', ugettext(u'zdravotní')),
        ('s', 'SOCIAL', ugettext(u'sociální')),
        ('f', 'MEDICAL_FACILITY', ugettext(u'léčebné zařízení')),
        ('o', 'OTHER', ugettext(u'jiné'))
    )
    where = MultiSelectField(max_length=10, choices=ASIST_TYPES, verbose_name=_(u'Kam'))
    note = models.TextField(null=True, blank=True, verbose_name=_(u'Poznámka'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Doprovod klienta')
        verbose_name_plural = _(u'Doprovod klientů')

    class Options:
        codenumber = 9
        limited_to = ('Client',)

    def _prepare_title(self):
        return _(u'%(title)s: %(where)s') % {
            'title': self.service.title, 'where': self.get_where_display()
        }


class InformationService(Service):
    safe_usage = models.BooleanField(default=False,
        verbose_name=_(u'1) bezpečné užívání'))
    safe_sex = models.BooleanField(default=False,
        verbose_name=_(u'2) bezpečný sex'))
    medical = models.BooleanField(default=False, verbose_name=_(u'3) zdravotní'))
    socio_legal = models.BooleanField(default=False,
        verbose_name=_(u'4) sociálně-právní'))
    cure_possibilities = models.BooleanField(default=False,
        verbose_name=_(u'5) možnosti léčby'))
    literature = models.BooleanField(default=False,
        verbose_name=_(u'6) tištěný informační materiál'))
    other = models.BooleanField(default=False, verbose_name=_(u'7) ostatní'))

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
    def _get_stats(cls, filtering):
        boolean_stats = _boolean_stats(cls, filtering, ('safe_usage', 'safe_sex',
            'medical', 'socio_legal', 'cure_possibilities', 'literature', 'other'))
        return chain( # The total count is computed differently than usually.
                ((cls.service.title, sum(stat[1] for stat in boolean_stats)),),
                boolean_stats,
        )


class ContactWork(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Kontaktní práce')
        verbose_name_plural = _(u'Kontaktní práce')

    class Options:
        codenumber = 4


class CrisisIntervention(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Pomoc v krizi')
        verbose_name_plural = _(u'Pomoci v krizi')

    class Options:
        codenumber = 7
        limited_to = ('Client',)


class SocialWork(Service):
    socio_legal = models.BooleanField(default=False,
        verbose_name=_(u'a) sociálně-právní'))
    counselling = models.BooleanField(default=False,
        verbose_name=_(u'b) předléčebné indiviuální poradenství'))
    service_mediation = models.BooleanField(default=False,
        verbose_name=_(u'c) zprostředkování dalších služeb'))
    other = models.BooleanField(default=False,
        verbose_name=_(u'd) jiná'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Případová práce')
        verbose_name_plural = _(u'Případové práce')

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
    def _get_stats(cls, filtering):
        return super(SocialWork, cls)._get_stats(filtering) + (
            _boolean_stats(cls, filtering, ('socio_legal', 'counselling',
                                            'service_mediation', 'other')))


class UtilityWork(Service):
    REF_TYPES = Choices(
        ('fp', 'FIELD_PROGRAMME', ugettext(u'1) Terenní programy')),
        ('cc', 'CONTACT_CENTER', ugettext(u'2) Kontaktní centrum')),
        ('mf', 'MEDICAL_FACILITY', ugettext(u'3) Léčebná zařízení')),
        ('ep', 'EXCHANGE_PROGRAMME', ugettext(u'4) Výměnný pogram')),
        ('t', 'TESTS', ugettext(u'5) Testy')),
        ('hs', 'HEALTHCARE_SERVICES', ugettext(u'6) Zdravotní služby')),
        ('ss', 'SOCIAL_SERVICES', ugettext(u'7) Sociální služby')),
        ('can', 'CANCEL', ugettext(u'8) Dohoduntý kontakt neproběhl / event. péče ukončena klientem bez dohody')),
        ('o', 'OTHER', ugettext(u'9) jiné'))
    )

    refs = MultiSelectField(max_length=40, choices=REF_TYPES, verbose_name=_(u'Odkazy'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Odkazy')
        verbose_name_plural = _(u'Odkazy')

    class Options:
        codenumber = 12

    @classmethod
    def _get_stats(cls, filtering):
        """Count all the items in all the MultiSelectFields."""
        objects = cls.objects.filter(**filtering)
        total_count = sum(len(address.refs) for address in objects)
        substats = defaultdict(int)
        for address in objects:
            for choice in address.refs:
                substats[choice] += 1
        return chain(
            ((cls.service.title, total_count),),
            ((choice[1], substats[choice[0]]) for choice in cls.REF_TYPES),
        )


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


class IncomeFormFillup(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Vyplnění IN-COME dotazníku')
        verbose_name_plural = _(u'Vyplnění IN-COME dotazníků')

    class Options:
        codenumber = 11
        limited_to = ('Client',)


class PhoneUsage(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        verbose_name = _(u'Použití telefonu klientem')
        verbose_name_plural = _(u'Použití telefonu klientem')

    class Options:
        codenumber = 15
        limited_to = ('Client',)