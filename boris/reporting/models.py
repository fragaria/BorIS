from django.db import models

from boris.clients.models import Person, Town, Client


class SearchEncounter(models.Model):
    """
    An augmented model corresponding to a database view.
    """
    person = models.ForeignKey(Person, related_name='+')
    performed_on = models.DateField()
    town = models.ForeignKey(Town, related_name='+')

    # derived attributes:
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()
    nr_of_addresses = models.SmallIntegerField()
    nr_of_incomeexaminations = models.SmallIntegerField()
    person_model = models.CharField(max_length=100)
    client_sex = models.SmallIntegerField()
    client = models.ForeignKey(Client, related_name='+')
    client_is_drug_user = models.BooleanField()
    client_iv = models.BooleanField()

    class Meta:
        managed = False
