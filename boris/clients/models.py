# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel
from model_utils import Choices

from boris.clients.classification import SEXES, APPLICATIONS, NATIONALITIES,\
    ETHNIC_ORIGINS, LIVING_CONDITIONS, ACCOMODATION_TYPES, EMPLOYMENT_TYPES,\
    EDUCATION_LEVELS, HIV_EXAMINATION_CLASSES, HEPATITIS_EXAMINATION_CLASSES,\
    DRUG_APPLICATION_FREQUENCY, DRUG_APPLICATION_TYPES


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
    
    # in-come anamnesis
    birthdate = models.DateField(blank=True, null=True, verbose_name=u'Datum narození')
    nationality = models.PositiveSmallIntegerField(choices=NATIONALITIES,
        blank=True, null=True, verbose_name=u'Státní příslušnost')
    ethnic_origin = models.PositiveSmallIntegerField(choices=ETHNIC_ORIGINS,
        blank=True, null=True, verbose_name=u'Etnická příslušnost')
    living_condition = models.PositiveSmallIntegerField(choices=LIVING_CONDITIONS,
        blank=True, null=True, verbose_name=u'Bydlení (s kým klient žije)')
    accomodation = models.PositiveSmallIntegerField(choices=ACCOMODATION_TYPES,
        blank=True, null=True, verbose_name=u'Bydlení (kde klient žije)')
    lives_with_junks = models.NullBooleanField(verbose_name=u'Žije klient s osobou užívající drogy')
    employment = models.PositiveSmallIntegerField(choices=EMPLOYMENT_TYPES,
        blank=True, null=True, verbose_name=u'Zaměstnání / škola')
    education = models.PositiveSmallIntegerField(choices=EDUCATION_LEVELS,
        blank=True, null=True, verbose_name=u'Vzdělání')
    hiv_examination = models.PositiveSmallIntegerField(choices=HIV_EXAMINATION_CLASSES,
        blank=True, null=True, verbose_name=u'Vyšetření HIV')
    hepatitis_examination = models.PositiveSmallIntegerField(
        choices=HEPATITIS_EXAMINATION_CLASSES, blank=True, null=True,
        verbose_name=u'Vyšetření hepatitidy')
    been_cured_before = models.NullBooleanField(verbose_name=u'Dříve léčen')
    been_cured_currently = models.NullBooleanField(verbose_name=u'Nyní léčen')
    town = models.ForeignKey(Town, verbose_name=u'Město')
    district = models.CharField(max_length=100, blank=True, null=True,
        verbose_name=u'Okres')
    region = models.CharField(max_length=100, blank=True,
        null=True, verbose_name=u'Kraj')
    
    drugs = models.ManyToManyField(Drug, through='DrugUsage',
        verbose_name=u'Užívané drogy')
    risky_manners = models.ManyToManyField(RiskyBehavior, through='RiskyManners',
        verbose_name=u'Riziková chování')

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
    client = models.ForeignKey(Client, verbose_name=u'Klient')
    
    application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=u'Aplikace')
    frequency = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_FREQUENCY,
        verbose_name=u'Četnost')
    first_try_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=u'První užití (věk)')
    first_try_iv_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=u'První i.v. užití (věk)')
    first_try_application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES,
        verbose_name=u'Způsob prvního užití')
    was_first_illegal = models.NullBooleanField(verbose_name=u'První neleg. droga')
    is_primary = models.BooleanField(verbose_name=u'Primární droga')
    note = models.TextField(null=True, blank=True, verbose_name=u'Poznámka')
    
    def __unicode__(self):
        return u'%s: %s' % (self.client, self.drug)
    
    class Meta:
        verbose_name = u'Užívaná droga'
        verbose_name_plural = u'Užívané drogy'
        
    
class RiskyManners(models.Model):
    OCCURENCES = Choices((1, 'ONCE', u'Jednorázově'), (2, 'RECURRING', u'Opakovaně'))
    
    behavior = models.ForeignKey(RiskyBehavior, verbose_name=u'Chování')
    client = models.ForeignKey(Client, verbose_name=u'Klient')
    
    past = models.PositiveSmallIntegerField(choices=OCCURENCES,
        null=True, blank=True, verbose_name=u'Minulost')
    present = models.PositiveSmallIntegerField(choices=OCCURENCES,
        null=True, blank=True, verbose_name=u'Současnost')
    never = models.NullBooleanField(verbose_name=u'Nikdy')

    @property
    def unknown(self):
        return all((self.past is None, self.present is None, self.never is None))

    def __unicode__(self):
        return u'%s: %s' % (self.client, self.behavior)
    
    class Meta:
        verbose_name = u'Rizikové chování'
        verbose_name = u'Riziková chování'
        