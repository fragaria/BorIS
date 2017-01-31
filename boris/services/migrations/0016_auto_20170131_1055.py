# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_socialwork'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialwork',
            options={'verbose_name': 'Soci\xe1ln\xed pr\xe1ce', 'verbose_name_plural': 'Soci\xe1ln\xed pr\xe1ce'},
        ),
        migrations.RemoveField(
            model_name='socialwork',
            name='counselling',
        ),
        migrations.RemoveField(
            model_name='socialwork',
            name='work_with_family',
        ),
        migrations.AddField(
            model_name='socialwork',
            name='assistance_service',
            field=models.BooleanField(default=False, verbose_name='d) asisten\u010dn\xed slu\u017eba'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialwork',
            name='probation_supervision',
            field=models.BooleanField(default=False, verbose_name='e) proba\u010dn\xed dohled'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='service_mediation',
            field=models.BooleanField(default=False, verbose_name='c) zprost\u0159edkov\xe1n\xed dal\u0161\xedch slu\u017eeb'),
            preserve_default=True,
        ),
    ]
