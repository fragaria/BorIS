# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20160415_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialwork',
            name='work_with_family',
            field=models.BooleanField(default=False, verbose_name='e) pr\xe1ce s rodinou'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='other',
            field=models.BooleanField(default=False, verbose_name='f) jin\xe1'),
            preserve_default=True,
        ),
    ]
