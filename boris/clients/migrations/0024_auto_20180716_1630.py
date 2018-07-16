# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from boris.reporting.management.install_views import install_views


def run_install_views(apps, schema_editor):
    install_views(None)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0023_auto_20180716_1615'),
        ('services', '0032_auto_20180619_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='sex_partner',
        ),
        migrations.AlterField(
            model_name='client',
            name='close_person',
            field=models.BooleanField(default=False, verbose_name='Osoba bl\xedzk\xe1 (rodi\u010de, sex. partne\u0159i apod.)'),
            preserve_default=True,
        ),
        migrations.RunPython(code=run_install_views, reverse_code=reverse),
    ]
