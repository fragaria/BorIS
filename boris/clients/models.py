# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

from boris.clients.classification import SEXES, NATIONALITIES,\
    ETHNIC_ORIGINS, LIVING_CONDITIONS, ACCOMODATION_TYPES, EMPLOYMENT_TYPES,\
    EDUCATION_LEVELS, HIV_EXAMINATION_CLASSES, HEPATITIS_EXAMINATION_CLASSES,\
    DRUG_APPLICATION_FREQUENCY, DRUG_APPLICATION_TYPES,\
    PRIMARY_DRUG_APPLICATION_TYPES, RISKY_BEHAVIOR_PERIODICITY


class StringEnum(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'Název')

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class Drug(StringEnum):
    class Meta:
        verbose_name = u'Droga'
        verbose_name_plural = u'Drogy'


class RiskyBehavior(StringEnum):
    class Meta:
        verbose_name = u'Rizikové chování'
        verbose_name_plural = u'Riziková chování'


class Town(StringEnum):
    class Meta:
        verbose_name = u'Město'
        verbose_name_plural = u'Města'


class Client(TimeStampedModel):
    code = models.CharField(max_length=63, unique=True, verbose_name=u'Kód')
    sex = models.PositiveSmallIntegerField(choices=SEXES, verbose_name=u'Pohlaví')
    first_name = models.CharField(max_length=63, blank=True, null=True, verbose_name=u'Jméno')
    last_name= models.CharField(max_length=63, blank=True, null=True, verbose_name=u'Příjmení')
    birthdate = models.DateField(blank=True, null=True, verbose_name=u'Datum narození')
    town = models.ForeignKey(Town, verbose_name=u'Město')
    primary_drug = models.ForeignKey(Drug, blank=True, null=True, verbose_name=u'Primární droga')
    primary_drug_usage = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=PRIMARY_DRUG_APPLICATION_TYPES, verbose_name=u'Způsob aplikace')

    @property
    def first_contact_date(self):
        pass

    @property
    def last_contact_date(self):
        pass

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = u'Klient'
        verbose_name_plural = u'Klienti'


class Anamnesis(TimeStampedModel):
    """ Income anamnesis. """

    client = models.OneToOneField(Client, verbose_name=u'Klient')
    filled_when = models.DateField(verbose_name=u'Datum kontaktu')
    filled_where = models.CharField(max_length=255, verbose_name=u'Místo kontaktu')
    author = models.ForeignKey(User, verbose_name=u'Vyplnil')

    nationality = models.PositiveSmallIntegerField(choices=NATIONALITIES,
        verbose_name=u'Státní příslušnost')
    ethnic_origin = models.PositiveSmallIntegerField(choices=ETHNIC_ORIGINS,
        verbose_name=u'Etnická příslušnost')
    living_condition = models.PositiveSmallIntegerField(choices=LIVING_CONDITIONS,
        verbose_name=u'Bydlení (s kým klient žije)')
    accomodation = models.PositiveSmallIntegerField(choices=ACCOMODATION_TYPES,
        verbose_name=u'Bydlení (kde klient žije)')
    lives_with_junkies = models.BooleanField(verbose_name=u'Žije klient s osobou užívající drogy?')
    employment = models.PositiveSmallIntegerField(choices=EMPLOYMENT_TYPES,
        verbose_name=u'Zaměstnání / škola')
    education = models.PositiveSmallIntegerField(choices=EDUCATION_LEVELS,
        verbose_name=u'Vzdělání')
    hiv_examination = models.PositiveSmallIntegerField(choices=HIV_EXAMINATION_CLASSES,
        verbose_name=u'Vyšetření HIV')
    hepatitis_examination = models.PositiveSmallIntegerField(
        choices=HEPATITIS_EXAMINATION_CLASSES, verbose_name=u'Vyšetření hepatitidy')
    been_cured_before = models.BooleanField(verbose_name=u'Dříve léčen')
    been_cured_currently = models.BooleanField(verbose_name=u'Nyní léčen')
    district = models.CharField(max_length=100, verbose_name=u'Okres')
    region = models.CharField(max_length=100, verbose_name=u'Kraj')

    drugs = models.ManyToManyField(Drug, through='DrugUsage',
        verbose_name=u'Užívané drogy')
    risky_manners = models.ManyToManyField(RiskyBehavior, through='RiskyManners',
        verbose_name=u'Riziková chování')

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
        return u'Anamnéza: %s' % self.client

    class Meta:
        verbose_name = u'Anamnéza'
        verbose_name_plural = u'Anamnézy'


class ClientNote(models.Model):
    author = models.ForeignKey(User, verbose_name=u'Autor')
    client = models.ForeignKey(Client, verbose_name=u'Klient')
    datetime = models.DateTimeField(default=datetime.datetime.now,
        verbose_name=u'Datum a čas')
    text = models.TextField(verbose_name=u'Text')

    def __unicode__(self):
        return "%s -> %s, %s" % (self.author, self.client,
                self.datetime.strftime("%Y-%m-%d %H:%M"))

    class Meta:
        verbose_name = u'Poznámka'
        verbose_name_plural = u'Poznámky'
        ordering = ('-datetime',)


class DrugUsage(models.Model):
    drug = models.ForeignKey(Drug, verbose_name=u'Droga')
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=u'Anamnéza')

    application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=u'Aplikace')
    frequency = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_FREQUENCY,
        verbose_name=u'Četnost')
    first_try_age = models.PositiveSmallIntegerField(
        verbose_name=u'První užití (věk)')
    first_try_iv_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=u'První i.v. užití (věk)')
    first_try_application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=u'Způsob prvního užití')
    was_first_illegal = models.NullBooleanField(verbose_name=u'První neleg. droga')
    is_primary = models.BooleanField(verbose_name=u'Primární droga')
    note = models.TextField(null=True, blank=True, verbose_name=u'Poznámka')

    def __unicode__(self):
        return u'%s: %s' % (self.anamnesis.client, self.drug)

    class Meta:
        verbose_name = u'Užívaná droga'
        verbose_name_plural = u'Užívané drogy'
        unique_together = ('drug', 'anamnesis')


class RiskyManners(models.Model):
    behavior = models.ForeignKey(RiskyBehavior, verbose_name=u'Chování')
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=u'Anamnéza')
    periodicity = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=RISKY_BEHAVIOR_PERIODICITY, verbose_name=u'Jak často')

    def __unicode__(self):
        return u'%s: %s' % (self.anamnesis.client, self.behavior)

    class Meta:
        verbose_name = u'Rizikové chování'
        verbose_name = u'Riziková chování'
        unique_together = ('behavior', 'anamnesis')

