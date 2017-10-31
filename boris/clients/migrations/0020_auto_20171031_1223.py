# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_terrainnotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=80, null=True, verbose_name='E-mail', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=models.IntegerField(max_length=20, null=True, verbose_name='Telefonn\xed \u010d\xedslo', blank=True),
            preserve_default=True,
        ),
    ]
