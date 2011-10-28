# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.utils.formats import get_format
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from fragapy.common.models.adminlink import AdminLinkMixin

from boris.clients.classification import SEXES, NATIONALITIES,\
    ETHNIC_ORIGINS, LIVING_CONDITIONS, ACCOMODATION_TYPES, EMPLOYMENT_TYPES,\
    DRUG_APPLICATION_FREQUENCY, DRUG_APPLICATION_TYPES,\
    PRIMARY_DRUG_APPLICATION_TYPES, RISKY_BEHAVIOR_PERIODICITY, DISEASES,\
    DISEASE_TEST_RESULTS, EDUCATION_LEVELS, DISEASE_TEST_SIGN


class StringEnum(models.Model):
    title = models.CharField(max_length=100, verbose_name=_(u'Název'))

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class Drug(StringEnum):
    class Meta:
        verbose_name = _(u'Droga')
        verbose_name_plural = _(u'Drogy')


class RiskyBehavior(StringEnum):
    class Meta:
        verbose_name = _(u'Rizikové chování')
        verbose_name_plural = _(u'Riziková chování')


class Region(StringEnum):
    class Meta:
        verbose_name = _(u'Kraj')
        verbose_name_plural = _(u'Kraje')


class District(StringEnum):
    region = models.ForeignKey(Region, verbose_name=_(u'Kraj'))

    class Meta:
        verbose_name = _(u'Okres')
        verbose_name_plural = _(u'Okresy')
        
    def __unicode__(self):
        return u'%s, %s' % (self.title, unicode(self.region)) 


class Town(StringEnum):
    district = models.ForeignKey(District, verbose_name=_(u'Okres'))

    class Meta:
        verbose_name = _(u'Město')
        verbose_name_plural = _(u'Města')
        
    def __unicode__(self):
        return u'%s (%s)' % (self.title, unicode(self.district)) 


class Client(TimeStampedModel, AdminLinkMixin):
    code = models.CharField(max_length=63, unique=True, verbose_name=_(u'Kód'))
    sex = models.PositiveSmallIntegerField(choices=SEXES, verbose_name=_(u'Pohlaví'))
    first_name = models.CharField(max_length=63, blank=True, null=True, verbose_name=_(u'Jméno'))
    last_name= models.CharField(max_length=63, blank=True, null=True, verbose_name=_(u'Příjmení'))
    birthdate = models.DateField(verbose_name=_(u'Datum narození'), blank=True, null=True,
        help_text=_(u'Pokud znáte pouze rok, zaškrtněte políčko `Známý pouze rok`.'))
    birthdate_year_only = models.BooleanField(default=True,
        verbose_name=_(u'Známý pouze rok'))
    town = models.ForeignKey(Town, verbose_name=_(u'Město'))
    primary_drug = models.ForeignKey(Drug, blank=True, null=True, verbose_name=_(u'Primární droga'))
    primary_drug_usage = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=PRIMARY_DRUG_APPLICATION_TYPES, verbose_name=_(u'Způsob aplikace'))

    @property
    def first_contact_date(self):
        try:
            return self.encounters.order_by('performed_on').values_list('performed_on', flat=True)[0]
        except IndexError:
            return None

    @property
    def last_contact_date(self):
        try:
            return self.encounters.order_by('-performed_on').values_list('performed_on', flat=True)[0]
        except IndexError:
            return None
        
    @property
    def services(self):
        from boris.services.models.core import ClientService
        return ClientService.objects.filter(encounter__client=self)

    def __unicode__(self):
        return self.code

    @permalink
    def get_admin_url(self):
        return ('admin:clients_client_change', (str(self.pk),))

    class Meta:
        verbose_name = _(u'Klient')
        verbose_name_plural = _(u'Klienti')


class Anamnesis(TimeStampedModel):
    """ Income anamnesis. """

    client = models.OneToOneField(Client, verbose_name=_(u'Klient'))
    filled_when = models.DateField(verbose_name=_(u'Datum kontaktu'))
    filled_where = models.ForeignKey(Town, verbose_name=_(u'Město kontaktu'))
    author = models.ForeignKey(User, verbose_name=_(u'Vyplnil'))

    nationality = models.PositiveSmallIntegerField(choices=NATIONALITIES,
        default=NATIONALITIES.UNKNOWN, verbose_name=_(u'Státní příslušnost'))
    ethnic_origin = models.PositiveSmallIntegerField(choices=ETHNIC_ORIGINS,
        default=ETHNIC_ORIGINS.NOT_MONITORED, verbose_name=_(u'Etnická příslušnost'))
    living_condition = models.PositiveSmallIntegerField(choices=LIVING_CONDITIONS,
        default=LIVING_CONDITIONS.UNKNOWN, verbose_name=_(u'Bydlení (s kým klient žije)'))
    accomodation = models.PositiveSmallIntegerField(choices=ACCOMODATION_TYPES,
        default=ACCOMODATION_TYPES.UNKNOWN, verbose_name=_(u'Bydlení (kde klient žije)'))
    lives_with_junkies = models.NullBooleanField(verbose_name=_(u'Žije klient s osobou užívající drogy?'))
    employment = models.PositiveSmallIntegerField(choices=EMPLOYMENT_TYPES,
        verbose_name=_(u'Zaměstnání / škola'))
    education = models.PositiveSmallIntegerField(choices=EDUCATION_LEVELS,
        verbose_name=_(u'Vzdělání'))
    been_cured_before = models.BooleanField(verbose_name=_(u'Dříve léčen'))
    been_cured_currently = models.BooleanField(verbose_name=_(u'Nyní léčen'))

    drugs = models.ManyToManyField(Drug, through='DrugUsage',
        verbose_name=_(u'Užívané drogy'))
    risky_manners = models.ManyToManyField(RiskyBehavior, through='RiskyManners',
        verbose_name=_(u'Riziková chování'))

    @property
    def birth_year(self):
        return self.client.birth_year

    @property
    def client_code(self):
        return self.client.code

    @property
    def sex(self):
        return self.client.sex

    def __unicode__(self):
        return _(u'Anamnéza: %s') % self.client

    @permalink
    def get_admin_url(self):
        return ('admin:clients_anamnesis_change', (str(self.pk),))

    class Meta:
        verbose_name = _(u'Anamnéza')
        verbose_name_plural = _(u'Anamnézy')


class ClientNote(models.Model):
    author = models.ForeignKey(User, verbose_name=_(u'Autor'),
        related_name='notes_added')
    client = models.ForeignKey(Client, verbose_name=_(u'Klient'),
        related_name='notes')
    datetime = models.DateTimeField(default=datetime.datetime.now,
        verbose_name=_(u'Datum a čas'))
    text = models.TextField(verbose_name=_(u'Text'))

    def __unicode__(self):
        return u"%s -> %s, %s" % (self.author, self.client,
            format(self.datetime, get_format('DATE_FORMAT')))

    class Meta:
        verbose_name = _(u'Poznámka')
        verbose_name_plural = _(u'Poznámky')
        ordering = ('-datetime', '-id')


class DrugUsage(models.Model):
    drug = models.ForeignKey(Drug, verbose_name=_(u'Droga'))
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=_(u'Anamnéza'))

    application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=_(u'Aplikace'))
    frequency = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_FREQUENCY,
        verbose_name=_(u'Četnost'))
    first_try_age = models.PositiveSmallIntegerField(
        verbose_name=_(u'První užití (věk)'))
    first_try_iv_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=_(u'První i.v. užití (věk)'))
    first_try_application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=_(u'Způsob prvního užití'))
    was_first_illegal = models.NullBooleanField(verbose_name=_(u'První neleg. droga'))
    is_primary = models.BooleanField(verbose_name=_(u'Primární droga'))
    note = models.TextField(null=True, blank=True, verbose_name=_(u'Poznámka'))

    def __unicode__(self):
        return unicode(self.drug)

    class Meta:
        verbose_name = _(u'Užívaná droga')
        verbose_name_plural = _(u'Užívané drogy')
        unique_together = ('drug', 'anamnesis')


class RiskyManners(models.Model):
    behavior = models.ForeignKey(RiskyBehavior, verbose_name=_(u'Chování'))
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=_(u'Anamnéza'))
    periodicity = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=RISKY_BEHAVIOR_PERIODICITY, verbose_name=_(u'Jak často'))

    def __unicode__(self):
        return u'%s: %s' % (self.anamnesis.client, self.behavior)

    class Meta:
        verbose_name = _(u'Rizikové chování')
        verbose_name_plural = _(u'Riziková chování')
        unique_together = ('behavior', 'anamnesis')


class DiseaseTest(models.Model):
    anamnesis = models.ForeignKey(Anamnesis)
    disease = models.PositiveSmallIntegerField(choices=DISEASES,
        verbose_name=_(u'Testované onemocnění'))
    result = models.PositiveSmallIntegerField(choices=DISEASE_TEST_RESULTS,
        default=DISEASE_TEST_RESULTS.UNKNOWN, verbose_name=_(u'Výsledek testu'))
    sign = models.CharField(max_length=1, choices=DISEASE_TEST_SIGN,
        default=DISEASE_TEST_SIGN.UNKNOWN, verbose_name=_(u'Stav'))

    def __unicode__(self):
        return unicode(self.disease)

    class Meta:
        verbose_name = _(u'Vyšetření na onemocnění')
        verbose_name_plural = _(u'Vyšetření na onemocnění')
        unique_together = ('disease', 'anamnesis')

