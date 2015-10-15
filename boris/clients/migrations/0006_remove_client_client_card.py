# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20150924_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_card',
        ),
    ]
