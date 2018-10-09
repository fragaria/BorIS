# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_close_person_for_sex_partners(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    sex_partners = Client.objects.filter(sex_partner=True)
    for client in sex_partners:
        client.close_person = True
        client.save()
    print 'Set close_person=True for %s clients previously marked as sex partners.' % sex_partners.count()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0022_auto_20180530_1234'),
    ]

    operations = [
        migrations.RunPython(code=set_close_person_for_sex_partners, reverse_code=reverse),
    ]
