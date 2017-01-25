# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20170125_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crisisintervention',
            options={'verbose_name': 'Krizov\xe1 intervence', 'verbose_name_plural': 'Krizov\xe1 intervence'},
        ),
        migrations.AlterModelOptions(
            name='incomeformfillup',
            options={'verbose_name': 'Vstupn\xed zhodnocen\xed stavu klienta', 'verbose_name_plural': 'Vstupn\xed zhodnocen\xed stavu klienta'},
        ),
    ]
