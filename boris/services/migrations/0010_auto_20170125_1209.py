# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20170110_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='is_by_phone',
            field=models.BooleanField(default=False, verbose_name='Nep\u0159\xedm\xfd kontakt (telefon, po\u0161ta, internet)'),
            preserve_default=True,
        ),
    ]
