from django.db import models

from boris.clients.models import Person, Town, Drug
from boris.services.models.core import Service, Encounter

class SearchEncounter(models.Model):
    """
    An augmented model corresponding to a database view.
    """
    person = models.ForeignKey(Person, related_name='+')
    town = models.ForeignKey(Town, related_name='+')
    is_client = models.BooleanField()
    is_anonymous = models.BooleanField()
    is_practitioner = models.BooleanField()
    client_sex = models.PositiveSmallIntegerField()
    primary_drug = models.ForeignKey(Drug, related_name='+')
    primary_drug_usage = models.PositiveSmallIntegerField()
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()

    class Meta:
        managed = False

class SearchService(models.Model):
    service = models.ForeignKey(Service, related_name='+')
    person = models.ForeignKey(Person, related_name='+')
    encounter = models.ForeignKey(Encounter, related_name='+')
    content_type_model = models.CharField(max_length=255)
    town = models.ForeignKey(Town, related_name='+')
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()

    class Meta:
        managed = False
