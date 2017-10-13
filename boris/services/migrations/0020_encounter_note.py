# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_workforclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='note',
            field=models.TextField(verbose_name='Pozn\xe1mka', blank=True),
            preserve_default=True,
        ),
    ]
