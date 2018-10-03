# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0023_auto_20180716_1615'),
        ('services', '0031_worktherapy_to_therapy'),
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
    ]
