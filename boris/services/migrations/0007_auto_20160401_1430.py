# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20160401_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='group_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='P\u0159idru\u017een\xe1 skupina', blank=True, to='clients.GroupContact', null=True),
            preserve_default=True,
        ),
    ]
