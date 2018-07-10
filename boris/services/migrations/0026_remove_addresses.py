# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def remove_addresses(apps, schema_editor):
    Address = apps.get_model("services", "Address")
    address_ct = ContentType.objects.get_by_natural_key("services", "address")
    # Address.objects.all().delete() would remove all Services!
    Address.objects.filter(content_type_id=address_ct.id).delete()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0025_address_to_approach'),
    ]

    operations = [
        migrations.RunPython(code=remove_addresses, reverse_code=reverse),
    ]
