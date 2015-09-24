# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150827_1014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientcard',
            options={'verbose_name': 'Klientsk\xe1 karta', 'verbose_name_plural': 'Klientsk\xe1 karta'},
        ),
        migrations.AlterField(
            model_name='clientcard',
            name='client',
            field=models.ForeignKey(related_name='client_card', to='clients.Client'),
            preserve_default=True,
        ),
    ]
