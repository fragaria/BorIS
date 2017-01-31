# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0016_auto_20170131_1055'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IndividualCounseling',
        ),
    ]
