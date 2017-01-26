# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_auto_20170125_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkWithFamily',
            fields=[
            ],
            options={
                'verbose_name': 'Pr\xe1ce s rodinou',
                'proxy': True,
                'verbose_name_plural': 'Pr\xe1ce s rodinami',
            },
            bases=('services.service',),
        ),
        migrations.AlterModelOptions(
            name='postusage',
            options={'verbose_name': 'Koresponden\u010dn\xed pr\xe1ce', 'verbose_name_plural': 'Koresponden\u010dn\xed pr\xe1ce'},
        ),
    ]
