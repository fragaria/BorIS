# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import boris.clients.models
import fragapy.common.models.adminlink


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_card',
            field=models.FileField(upload_to=boris.clients.models.get_client_card_filename, null=True, verbose_name='Klientsk\xe1 karta', blank=True),
            preserve_default=True,
        ),
    ]
