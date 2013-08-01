from django.db import models

from boris.clients.models import Person, Town, Drug
from boris.services.models.core import Service, Encounter

DO_NOTHING = models.DO_NOTHING


class SearchEncounter(models.Model):
    """
    An augmented model corresponding to a database view.
    """
    person = models.ForeignKey(Person, related_name='+', on_delete=DO_NOTHING)
    town = models.ForeignKey(Town, related_name='+', on_delete=DO_NOTHING)
    is_client = models.BooleanField()
    is_anonymous = models.BooleanField()
    is_close_person = models.BooleanField()
    is_sex_partner = models.BooleanField()
    is_by_phone = models.BooleanField()
    client_sex = models.PositiveSmallIntegerField()
    primary_drug = models.ForeignKey(Drug, related_name='+', on_delete=DO_NOTHING)
    primary_drug_usage = models.PositiveSmallIntegerField()
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()

    class Meta:
        managed = False


class SearchService(models.Model):
    service = models.ForeignKey(Service, related_name='+', on_delete=DO_NOTHING)
    person = models.ForeignKey(Person, related_name='+', on_delete=DO_NOTHING)
    encounter = models.ForeignKey(Encounter, related_name='+', on_delete=DO_NOTHING)
    content_type_model = models.CharField(max_length=255)
    town = models.ForeignKey(Town, related_name='+', on_delete=DO_NOTHING)
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()
    is_client = models.BooleanField()
    is_anonymous = models.BooleanField()

    class Meta:
        managed = False


class SearchSyringeCollection(models.Model):
    count = models.SmallIntegerField()
    town = models.ForeignKey(Town, related_name='+', on_delete=DO_NOTHING)
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()

    class Meta:
        managed = False
