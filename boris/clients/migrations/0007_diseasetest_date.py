# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_remove_client_client_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseasetest',
            name='date',
            field=models.DateField(null=True, verbose_name='Datum', blank=True),
            preserve_default=True,
        ),
    ]
