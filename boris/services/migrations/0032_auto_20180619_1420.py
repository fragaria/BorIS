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
        ('services', '0031_worktherapy_to_therapy'),
    ]

    operations = [
        migrations.RunPython(code=run_install_views, reverse_code=reverse),
    ]
