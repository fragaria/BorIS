# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


TYPES = [
    (u'doléčovací', 7),
]


def create_types(apps, schema_editor):
    GroupContactType = apps.get_model("clients", "GroupContactType")
    for _type in TYPES:
        t, _ = GroupContactType.objects.get_or_create(title=_type[0], key=_type[1])
        t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_auto_20171031_1341'),
    ]

    operations = [
        migrations.RunPython(create_types),
    ]
