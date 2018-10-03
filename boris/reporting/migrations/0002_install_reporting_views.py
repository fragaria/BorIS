# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from boris.reporting.management.install_views import install_views


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
        ('clients', '0024_auto_20180716_1630'),
        ('services', '0031_worktherapy_to_therapy'),
        ('syringes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(install_views),
    ]
