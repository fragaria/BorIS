# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_diseasetest_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasetest',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True, verbose_name='Datum', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='diseasetest',
            unique_together=set([]),
        ),
    ]
