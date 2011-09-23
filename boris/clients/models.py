# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User


class Drug(models.Model):
    name = models.CharField(max_length=63, verbose_name=u'Jméno')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Droga'
        verbose_name_plural = u'Drogy'


class Town(models.Model):
    name = models.CharField(max_length=63, verbose_name=u'Jméno')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Město'
        verbose_name_plural = u'Města'


class Client(models.Model):
    SEX_FEMALE = 1
    SEX_MALE = 2
    SEX_CHOICES = (
        (SEX_FEMALE, u'žena'),
        (SEX_MALE, u'muž'),
    )

    APPLICATION_IV = 1
    APPLICATION_NONIV= 2
    APPLICATION_CHOICES = (
        (APPLICATION_IV, u'IV'),
        (APPLICATION_NONIV, u'neIV'),
    )

    code = models.CharField(max_length=63, unique=True, verbose_name=u'Kód')
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, verbose_name=u'Pohlaví')
    first_name = models.CharField(max_length=63, blank=True, null=True, verbose_name=u'Jméno')
    last_name= models.CharField(max_length=63, blank=True, null=True, verbose_name=u'Příjmení')
    birthdate = models.DateField(blank=True, null=True, verbose_name=u'Datum narození')
    town = models.ForeignKey(Town, verbose_name=u'Město')
    primary_drug = models.ForeignKey(Drug, verbose_name=u'Primární droga')
    application = models.PositiveSmallIntegerField(choices=APPLICATION_CHOICES, blank=True, null=True, verbose_name=u'Způsob aplikace')

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = u'Klient'
        verbose_name_plural = u'Klienti'


class ClientNote(models.Model):
    author = models.ForeignKey(User, verbose_name=u'Autor')
    client = models.ForeignKey(Client, verbose_name=u'Klient')
    datetime = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Datum a čas')
    text = models.TextField(verbose_name=u'Text')

    def __unicode__(self):
        return "%s -> %s, %s" % (self.author, self.client,
                self.datetime.strftime("%Y-%m-%d %H:%M"))

    class Meta:
        verbose_name = u'Poznámka'
        verbose_name_plural = u'Poznámky'


