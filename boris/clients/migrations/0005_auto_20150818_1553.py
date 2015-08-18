# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import boris.clients.models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_card',
            field=models.FileField(upload_to=boris.clients.models.get_client_card_filename, null=True, verbose_name='Klientsk\xe1 karta', blank=True),
            preserve_default=True,
        ),
    ]
