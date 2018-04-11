# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from itertools import chain


def clear_drugs_for_nonusers(apps, schema_editor):
    clients = apps.get_model("clients", "Client")
    clients = clients.objects.all()
    sex_partners = clients.filter(sex_partner=True)
    close_person = clients.filter(close_person=True)
    relatives = chain(sex_partners, close_person)
    count = 0
    for relative in relatives:
        relative.primary_drug = None
        relative.save()
        count += 1
    print 'Successfully set primary drugs to None for %d sex partners and close persons' % count


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0023_auto_20171027_1724'),
    ]

    operations = [
        migrations.RunPython(clear_drugs_for_nonusers),
    ]
