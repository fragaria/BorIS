# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.dateformat import format
from django.utils.formats import date_format, get_format
from django.utils.translation import ugettext_lazy as _
from fragapy.common.models.adminlink import AdminLinkMixin
from model_utils.models import TimeStampedModel

from boris.classification import SEXES, NATIONALITIES, \
    ETHNIC_ORIGINS, LIVING_CONDITIONS, ACCOMODATION_TYPES, EMPLOYMENT_TYPES, \
    DRUG_APPLICATION_FREQUENCY, DRUG_APPLICATION_TYPES, \
    DISEASES, DISEASE_TEST_RESULTS, EDUCATION_LEVELS, ANONYMOUS_TYPES, \
    RISKY_BEHAVIOR_KIND, RISKY_BEHAVIOR_PERIODICITY, DRUGS
from boris.services.models import GroupCounselling, Encounter
from boris.services.models.k import _group_service_title


class IndexedStringEnum(models.Model, AdminLinkMixin):
    title = models.CharField(max_length=100, verbose_name=_(u'Název'), db_index=True)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ('title__icontains',)


class Region(IndexedStringEnum):
    class Meta:
        verbose_name = _(u'Kraj')
        verbose_name_plural = _(u'Kraje')


class District(IndexedStringEnum):
    region = models.ForeignKey(Region, verbose_name=_(u'Kraj'))

    class Meta:
        verbose_name = _(u'Okres')
        verbose_name_plural = _(u'Okresy')

    def __unicode__(self):
        return u'%s, %s' % (self.title, unicode(self.region))


class Town(IndexedStringEnum):
    district = models.ForeignKey(District, verbose_name=_(u'Okres'))

    class Meta:
        verbose_name = _(u'Město')
        verbose_name_plural = _(u'Města')

    def __unicode__(self):
        return u'%s' % self.title


class GroupContactType(IndexedStringEnum):
    key = models.SmallIntegerField(verbose_name=_(u'Kód'))

    class Meta:
        verbose_name = _(u'Typ skupiny')
        verbose_name_plural = _(u'Typy skupin')

    def __unicode__(self):
        return u'%s) %s' % (self.key, unicode(self.title))


class Person(TimeStampedModel, AdminLinkMixin):
    # title enables us to easily print subclass __unicode__ values from Person
    title = models.CharField(max_length=255, editable=False,
        verbose_name=_(u'Název'), db_index=True)
    content_type = models.ForeignKey(ContentType, editable=False)

    class Meta:
        verbose_name = _(u'Osoba')
        verbose_name_plural = _(u'Osoby')

    @property
    def services(self):
        from boris.services.models.core import Service
        return Service.objects.filter(encounter__person=self)

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

    def __unicode__(self):
        return self.title

    def clean(self):
        self.title = unicode(self)
        # @attention: instead of using get_for_model which doesn't respect
        # proxy models content types, use get_by_natural key as a workaround
        self.content_type = ContentType.objects.get_by_natural_key(
            self._meta.app_label, self._meta.object_name.lower())

    def cast(self):
        """
        When dealing with subclass that has been selected from base table,
        this will return the corresponding subclass instance.
        """
        try:
            return self.content_type.get_object_for_this_type(pk=self.pk)
        except ContentType.DoesNotExist:  # E.g. mock objects or some not-yet-saved objects.
            return self

    def is_default_service(self, service):
        """Returns True if ``service`` is default for this person, False otherwise"""
        return False

    @staticmethod
    def autocomplete_search_fields():
        return ('title__icontains',)


class PractitionerContact(models.Model, AdminLinkMixin):
    '''
    A simple model to capture the contacts with practitioners.

    (Formerly was a descendant of Person named "Practitioner".)

    '''
    users = models.ManyToManyField('auth.User', verbose_name=_('Kdo'))
    person_or_institution = models.CharField(max_length=255,
        verbose_name=_(u'Osoba nebo instituce'))
    town = models.ForeignKey('clients.Town', related_name='+', verbose_name=_(u'Město'))
    date = models.DateField(verbose_name=_(u'Kdy'))
    note = models.TextField(verbose_name=_(u'Poznámka'), blank=True)

    class Meta:
        verbose_name = _(u'Odborný kontakt')
        verbose_name_plural = _(u'Odborné kontakty')

    def __unicode__(self):
        return _(u'%(person_or_institution)s v %(town)s, %(date)s') % {
            'person_or_institution': self.person_or_institution,
            'town': self.town,
            'date': date_format(self.date)
        }


class GroupContact(models.Model, AdminLinkMixin):
    '''
    A model for convenient work with group counselling service.
    '''
    users = models.ManyToManyField('auth.User', verbose_name=_('Kdo'))
    clients = models.ManyToManyField('clients.Client', verbose_name=_('Klienti'))
    town = models.ForeignKey('clients.Town', related_name='+', verbose_name=_(u'Město'))
    date = models.DateField(verbose_name=_(u'Kdy'))
    note = models.TextField(verbose_name=_(u'Poznámka'), blank=True)
    type = models.ForeignKey('clients.GroupContactType', related_name='+', verbose_name=_(u'Typ'),
                             default=1)

    class Meta:
        verbose_name = u'Skupinový kontakt'
        verbose_name_plural = u'Skupinové kontakty'

    def __unicode__(self):
        town = self.town.title if hasattr(self, 'town') and self.town else '---'
        return u'Skupinový kontakt %s, %s, %s' % (self.type.title, town, self.date)


def __sync_many(e, instance, src_attr, target_attr):
    existing = getattr(e, src_attr).values_list('id', flat=True)
    to_keep = getattr(instance, target_attr).values_list('id', flat=True)
    to_delete = set(existing) - set(to_keep)
    to_create = set(to_keep) - set(existing)
    for pk in to_create:
        getattr(e, src_attr).add(pk)
    for pk in to_delete:
        getattr(e, src_attr).remove(pk)


def __get_or_create_encounter(client, instance, services):
    e, created = Encounter.objects.get_or_create(person=client, is_by_phone=False, group_contact=instance,
                                                 defaults={'performed_on': instance.date, 'where': instance.town})
    __sync_many(e, instance, 'performed_by', 'users')
    e.performed_on = instance.date
    e.where = instance.town
    e.save()

    for service in services:
        ct = service.service.model.real_content_type()
        s, _ = service.objects.get_or_create(encounter=e, content_type=ct)
        s.title = _group_service_title(instance, service)
        s.save()
    return e, created


def __delete_group_encounters(encs, group_contact):
    for encounter in encs:
        services = encounter.services.all()
        group_services = __filter_group_services(group_contact, services)
        if services.count() == 1 and group_services.exists():
            encounter.delete()
        else:
            group_services.delete()


def __filter_group_services(group_contact, services):
    return services.filter(content_type=GroupCounselling.real_content_type())


def __correct_contact(encs, instance):
    for encounter in encs:
        for service in __filter_group_services(instance, encounter.services):
            service.save()
        encounter.save()


@receiver(signals.m2m_changed, sender=GroupContact.clients.through)
def create_group_encounters(sender, instance, action, *args, **kwargs):
    # group contact serves as a way to create many group counselling encounters at a time
    # this signal is used for creating encounters
    for client in instance.clients.all():
        __get_or_create_encounter(client, instance, [GroupCounselling])
    if instance.clients.exists():
        # this is needed because django sends signals pretty erratically :(
        delete_excess_group_encounters(sender, instance)


@receiver(signals.post_save, sender=GroupContact)
def delete_excess_group_encounters(sender, instance, *args, **kwargs):
    # this signal is used for deleting encounters for removed clients
    all_encs = Encounter.objects.filter(group_contact=instance)
    to_delete = set(all_encs.values_list('person', flat=True)) - set(instance.clients.values_list('pk', flat=True))
    for client_pk in to_delete:
        encs = all_encs.filter(person__pk=client_pk)
        __delete_group_encounters(encs, instance)


@receiver(signals.pre_delete, sender=GroupContact)
def save_group_contact3(sender, instance, using, signal, *args, **kwargs):
    encs = Encounter.objects.filter(group_contact=instance)
    __delete_group_encounters(encs, instance)


class Anonymous(Person):
    drug_user_type = models.PositiveSmallIntegerField(
        choices=ANONYMOUS_TYPES, verbose_name=_(u'Typ'))
    sex = models.PositiveSmallIntegerField(choices=SEXES, verbose_name=_(u'Pohlaví'))

    class Meta:
        verbose_name = _(u'Anonym')
        verbose_name_plural = _(u'Anonymové')
        unique_together = ('sex', 'drug_user_type')

    def __unicode__(self):
        return u'%s - %s' % (self.get_sex_display(), self.get_drug_user_type_display())

    def is_default_service(self, service):
        """Returns True if ``service`` is default for this person, False otherwise"""
        return service.class_name() == 'Address'


class ClientManager(models.Manager):
    def filter_by_age(self, age_from=None, age_to=None):
        today = datetime.date.today()
        clients = self.all()
        if age_from is not None:
            born_to = today - relativedelta(years=age_from)
            clients = clients.filter(birthdate__lte=born_to)
        if age_to is not None:
            born_from = today - relativedelta(years=age_to + 1)
            clients = clients.filter(birthdate__gt=born_from)
        return clients


class Client(Person):
    code = models.CharField(max_length=63, unique=True, verbose_name=_(u'Kód'))
    sex = models.PositiveSmallIntegerField(choices=SEXES, verbose_name=_(u'Pohlaví'))
    first_name = models.CharField(max_length=63, blank=True, null=True,
        verbose_name=_(u'Jméno'))
    last_name = models.CharField(max_length=63, blank=True, null=True,
        verbose_name=_(u'Příjmení'))
    birthdate = models.DateField(verbose_name=_(u'Datum narození'), blank=True, null=True,
        help_text=_(u'Pokud znáte pouze rok, zaškrtněte políčko `Známý pouze rok`.'))
    birthdate_year_only = models.BooleanField(default=False,
        verbose_name=_(u'Známý pouze rok'))
    town = models.ForeignKey(Town, verbose_name=_(u'Město'))
    primary_drug = models.PositiveSmallIntegerField(blank=True, null=True,
            choices=DRUGS, verbose_name=_(u'Primární droga'))
    primary_drug_usage = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=DRUG_APPLICATION_TYPES, verbose_name=_(u'Způsob aplikace'))
    close_person = models.BooleanField(default=False,
        verbose_name=_(u'Osoba blízká (rodiče apod.)'))
    sex_partner = models.BooleanField(default=False,
        verbose_name=_(u'Sexuální partner'))
    phone_number = models.IntegerField(max_length=20, blank=True, null=True, verbose_name=_(u'Telefonní číslo'))
    email = models.EmailField(max_length=80, blank=True, null=True, verbose_name=_(u'E-mail'))

    class Meta:
        verbose_name = _(u'Klient')
        verbose_name_plural = _(u'Klienti')

    objects = ClientManager()

    def __unicode__(self):
        return self.code

    @property
    def age(self):
        """Return the client's age in years, if known."""
        if not self.birthdate:
            return None
        age = datetime.date.today() - self.birthdate
        return int(round(age.days / 365.2425)) - 1

    @property
    def hygiene_report_code(self):
        code = (str(self.birthdate.year)[2:] if self.birthdate else '??') + '0000/'
        code += self.code[5:8].upper() if len(self.code) >= 7 else '???'
        return code

    def is_default_service(self, service):
        """Returns True if ``service`` is default for this person, False otherwise"""
        return service.class_name() == 'HarmReduction'

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()
        super(Client, self).save(*args, **kwargs)


class Anamnesis(TimeStampedModel, AdminLinkMixin):
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
        default=EMPLOYMENT_TYPES.UNKNOWN, verbose_name=_(u'Zaměstnání / škola'))
    education = models.PositiveSmallIntegerField(choices=EDUCATION_LEVELS,
        default=EDUCATION_LEVELS.UNKNOWN, verbose_name=_(u'Vzdělání'))
    been_cured_before = models.BooleanField(verbose_name=_(u'Dříve léčen'), default=None)
    been_cured_currently = models.BooleanField(verbose_name=_(u'Nyní léčen'), default=None)

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

    class Meta:
        verbose_name = _(u'Anamnéza')
        verbose_name_plural = _(u'Anamnézy')

    @property
    def drug_info(self):
        if not hasattr(self, '__drug_info'):
            self.__drug_info =  DrugUsage.objects.filter(anamnesis=self)
            self.__drug_info = sorted(list(self.__drug_info),
                                      key=lambda di: '%s%s' % (
                                          '1' if di.is_primary else '2',
                                          str(di.pk)
                                      ))
        return self.__drug_info

    @property
    def disease_test_results(self):
        if not hasattr(self, '__disease_test_results'):
            self.__disease_test_results = dict((c[1], None) for c in DISEASE_TEST_RESULTS)

            for t in DiseaseTest.objects.filter(anamnesis=self):
                self.__disease_test_results[t.get_disease_display()] = t
        return self.__disease_test_results

    @property
    def overall_first_try_age(self):
        if not hasattr(self, '__overall_first_try_age'):
            ages = [d.first_try_age for d in self.drug_info]
            self.__overall_first_try_age = min(ages) if ages else None
        return self.__overall_first_try_age

    @property
    def is_intravenous_user(self):
        return any([di.application in (DRUG_APPLICATION_TYPES.VEIN_INJECTION,
                                       DRUG_APPLICATION_TYPES.MUSCLE_INJECTION)
                    for di in self.drug_info])

    @property
    def intravenous_first_try_age(self):
        if not hasattr(self, '__intravenous_first_try_age'):
            ages = [d.first_try_iv_age for d in self.drug_info if d.first_try_iv_age]
            self.__intravenous_first_try_age = min(ages) if ages else None
        return self.__intravenous_first_try_age


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
    drug = models.PositiveSmallIntegerField(choices=DRUGS, verbose_name=_(u'Droga'))
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=_(u'Anamnéza'))

    application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES, null=True, blank=True,
        verbose_name=_(u'Aplikace'))
    frequency = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_FREQUENCY, null=True, blank=True,
        verbose_name=_(u'Četnost'))
    first_try_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=_(u'První užití (věk)'))
    first_try_iv_age = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=_(u'První i.v. užití (věk)'))
    first_try_application = models.PositiveSmallIntegerField(choices=DRUG_APPLICATION_TYPES, null=True, blank=True,
        verbose_name=_(u'Způsob prvního užití'))
    was_first_illegal = models.NullBooleanField(verbose_name=_(u'První neleg. droga'))
    is_primary = models.BooleanField(verbose_name=_(u'Primární droga'), default=None)
    note = models.TextField(null=True, blank=True, verbose_name=_(u'Poznámka'))

    def __unicode__(self):
        return unicode(self.get_drug_display())

    class Meta:
        verbose_name = _(u'Užívaná droga')
        verbose_name_plural = _(u'Užívané drogy')
        unique_together = ('drug', 'anamnesis')


class RiskyManners(models.Model):
    behavior = models.PositiveIntegerField(choices=RISKY_BEHAVIOR_KIND)
    anamnesis = models.ForeignKey(Anamnesis, verbose_name=_(u'Anamnéza'))
    periodicity_in_past = models.PositiveIntegerField(blank=True, null=True,
        choices=RISKY_BEHAVIOR_PERIODICITY,
        verbose_name=_(u'Jak často v minulosti'))
    periodicity_in_present = models.PositiveIntegerField(blank=True, null=True,
        choices=RISKY_BEHAVIOR_PERIODICITY,
        verbose_name=_(u'Jak často v přítomnosti'))

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
    result = models.SmallIntegerField(choices=DISEASE_TEST_RESULTS,
        default=DISEASE_TEST_RESULTS.UNKNOWN, verbose_name=_(u'Výsledek testu'))
    date = models.DateField(verbose_name=_(u'Datum'), null=True, blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return unicode(self.disease)

    class Meta:
        verbose_name = _(u'Vyšetření onemocnění')
        verbose_name_plural = _(u'Vyšetření onemocnění')


def get_client_card_filename(instance, filename):
    return 'client_notes/%s/%s' % (instance.client.pk, filename)


class ClientCard(models.Model):
    client = models.ForeignKey(Client, related_name='client_card')
    file = models.FileField(upload_to=get_client_card_filename)

    class Meta:
        verbose_name = u'Přílohy'  # makes more sense from user's perspective
        verbose_name_plural = u'Přílohy'

    def save(self, *args, **kwargs):
        try:
            old_instance = ClientCard.objects.get(id=self.id)
            if old_instance.file != self.file:
                old_instance.file.delete(save=False)
        except ClientCard.DoesNotExist:
            pass

        super(ClientCard, self).save(*args, **kwargs)

    def delete(self, using=None):
        self.file.delete(save=False)
        super(ClientCard, self).delete(using=using)


class TerrainNotes(models.Model, AdminLinkMixin):
    users = models.ManyToManyField('auth.User', verbose_name=_('Kdo'))
    town = models.ForeignKey('clients.Town', related_name='+', verbose_name=_(u'Město'))
    date = models.DateField(verbose_name=_(u'Kdy'))
    note = models.TextField(verbose_name=_(u'Zápis'), blank=True)

    class Meta:
        verbose_name = _(u'Zápis z terénu')
        verbose_name_plural = _(u'Zápisy z terénu')
