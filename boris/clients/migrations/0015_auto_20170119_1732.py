# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_auto_20170119_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymous',
            name='drug_user_type',
            field=models.PositiveSmallIntegerField(verbose_name='Typ', choices=[(1, 'neu\u017eivatel'), (2, 'neIV'), (3, 'IV'), (4, 'rodi\u010d'), (5, 'THC')]),
            preserve_default=True,
        ),
    ]
