# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


TYPES = [
    (u'vzdělávací', 1),
    (u'pracovní', 2),
    (u'motivační', 3),
    (u'terapeutická', 4),
    (u'prevence relapsu', 5),
    (u'kulturní', 6),
]


def create_types(apps, schema_editor):
    GroupContactType = apps.get_model("clients", "GroupContactType")
    for _type in TYPES:
        t, _ = GroupContactType.objects.get_or_create(title=_type[0], key=_type[1])
        t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20160415_2044'),
    ]

    operations = [
        migrations.RunPython(create_types),
    ]
