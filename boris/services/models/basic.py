# -*- coding: utf-8 -*-
'''
Created on 2.10.2011

@author: xaralis
'''
from collections import defaultdict
from itertools import chain

from django.conf import settings
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
    capsule_count = models.PositiveIntegerField(default=0, verbose_name=_(u'počet vydaných kapslí'))

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
                               'capsule_count', 'encounter'),
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
    def _get_stats(cls, filtering, only_subservices=False):
        services = super(HarmReduction, cls)._get_stats(filtering, only_subservices)
        if only_subservices:
            return cls._get_subservices(filtering)
        return chain(services, cls._get_subservices(filtering))

    @classmethod
    def _get_subservices(cls, filtering):
        return chain(
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
            ((_(u'Počet vydaných kapslí'), _sum_int(cls, filtering,
                                                    'capsule_count')),),
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

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False):
        objects = cls.objects.filter(**filtering)
        total_count = objects.count()
        substats = defaultdict(int)
        for sign in DISEASE_TEST_SIGN:
            substats[sign[0]] = objects.filter(sign=sign[0]).count()
        subservices = ((choice[1], substats[choice[0]]) for choice in DISEASE_TEST_SIGN)
        if only_subservices:
            return chain(subservices)
        return chain(
            ((cls.service.title, total_count),),
            subservices,
        )


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
    def _get_stats(cls, filtering, only_subservices=False):
        boolean_stats = _boolean_stats(cls, filtering, ('safe_usage', 'safe_sex',
            'medical', 'socio_legal', 'cure_possibilities', 'literature', 'other'))
        if only_subservices:
            return chain(boolean_stats)
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
        verbose_name = _(u'Krizová intervence')
        verbose_name_plural = _(u'Krizová intervence')

    class Options:
        codenumber = 7
        limited_to = ('Client',)


class SocialWork(Service):
    social = models.BooleanField(default=False,
        verbose_name=_(u'a) sociální'))
    legal = models.BooleanField(default=False,
        verbose_name=_(u'b) trestně-právní'))
    service_mediation = models.BooleanField(default=False,
        verbose_name=_(u'c) zprostředkování dalších služeb'))
    assistance_service = models.BooleanField(default=False,
        verbose_name=_(u'd) asistenční služba'))
    probation_supervision = models.BooleanField(default=False,
        verbose_name=_(u'e) probační dohled'))
    other = models.BooleanField(default=False,
        verbose_name=_(u'f) jiná'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Sociální práce')
        verbose_name_plural = _(u'Sociální práce')

    class Options:
        codenumber = 6
        limited_to = ('Client',)
        fieldsets = (
            (None, {
                'fields': ('encounter', 'social', 'legal', 'service_mediation',
                            'assistance_service', 'probation_supervision', 'other'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False):
        service = super(SocialWork, cls)._get_stats(filtering, only_subservices)
        subservices = (_boolean_stats(cls, filtering, (
            'social', 'legal', 'service_mediation', 'assistance_service', 'probation_supervision', 'other')))
        if only_subservices:
            return subservices
        return service + subservices


class UtilityWork(Service):
    REF_TYPES = Choices(*[(c[0], c[1], ugettext(c[2])) for c in settings.UTILITY_WORK_CHOICES])

    refs = MultiSelectField(max_length=40, choices=REF_TYPES, verbose_name=_(u'Odkazy'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Odkazy')
        verbose_name_plural = _(u'Odkazy')

    class Options:
        codenumber = 12

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False):
        """Count all the items in all the MultiSelectFields."""
        objects = cls.objects.filter(**filtering)
        total_count = sum(len(address.refs) for address in objects)
        substats = defaultdict(int)
        for address in objects:
            for choice in address.refs:
                substats[choice] += 1
        subservices = ((choice[1], substats[choice[0]]) for choice in cls.REF_TYPES)
        if only_subservices:
            return chain(subservices)
        return chain(
            ((cls.service.title, total_count),),
            subservices,
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


class IndividualCounselling(Service):
    general = models.BooleanField(default=False,
        verbose_name=_(u'a) obecné'))
    structured = models.BooleanField(default=False,
        verbose_name=_(u'b) strukturované'))
    pre_treatment = models.BooleanField(default=False,
        verbose_name=_(u'c) předléčebné poradenství'))
    guarantee_interview = models.BooleanField(default=False,
        verbose_name=_(u'd) garantský pohovor'))
    advice_to_parents = models.BooleanField(default=False,
        verbose_name=_(u'e) poradenství pro rodiče/osoby blízké'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Individuální poradenství')
        verbose_name_plural = _(u'Individuální poradenství')

    class Options:
        codenumber = 5
        limited_to = ('Client',)
        fieldsets = (
            (None, {
                'fields': ('encounter', 'general', 'structured',
                           'pre_treatment', 'guarantee_interview', 'advice_to_parents'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False):
        service = super(IndividualCounselling, cls)._get_stats(filtering, only_subservices)
        subservices = (_boolean_stats(cls, filtering, (
            'general', 'structured', 'pre_treatment', 'guarantee_interview', 'advice_to_parents')))
        if only_subservices:
            return subservices
        return service + subservices


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
        verbose_name = _(u'Vstupní zhodnocení stavu klienta')
        verbose_name_plural = _(u'Vstupní zhodnocení stavu klienta')

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
        codenumber = 14
        limited_to = ('Client',)


class WorkForClient(Service):
    contact_institution = models.BooleanField(default=False,
        verbose_name=_(u'a) kontakt s institucemi'))
    message = models.BooleanField(default=False,
        verbose_name=_(u'b) zpráva, doporučení'))
    search_information = models.BooleanField(default=False,
        verbose_name=_(u'c) vyhledávání a zjišťování informací pro klienta'))
    case_conference = models.BooleanField(default=False,
        verbose_name=_(u'd) případová konference'))

    class Meta:
        app_label = 'services'
        verbose_name = _(u'Práce ve prospěch klienta')
        verbose_name_plural = _(u'Práce ve prospěch klienta')

    class Options:
        codenumber = 28
        form_template = 'services/forms/small_cells.html'
        fieldsets = (
            (None, {
                'fields': ('encounter', 'contact_institution', 'message', 'search_information',
                    'case_conference'),
                'classes': ('inline',)
            }),
        )

    @classmethod
    def _get_stats(cls, filtering, only_subservices=False):
        boolean_stats = _boolean_stats(cls, filtering, ('contact_institution', 'message',
            'search_information', 'case_conference'))
        if only_subservices:
            return chain(boolean_stats)
        return chain( # The total count is computed differently than usually.
                ((cls.service.title, sum(stat[1] for stat in boolean_stats)),),
                boolean_stats,
        )