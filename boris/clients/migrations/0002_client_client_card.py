# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_card',
            field=models.FileField(upload_to=b'client_notes', null=True, verbose_name='Klientsk\xe1 karta', blank=True),
            preserve_default=True,
        ),
    ]
