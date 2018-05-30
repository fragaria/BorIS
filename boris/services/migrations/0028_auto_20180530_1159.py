# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0027_auto_20180411_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indirectservice',
            name='service_ptr',
        ),
        migrations.DeleteModel(
            name='IndirectService',
        ),
        migrations.CreateModel(
            name='IndirectService',
            fields=[
            ],
            options={
                'verbose_name': 'Telefonick\xe9, p\xedsemn\xe9 a internetov\xe9 p.',
                'proxy': True,
                'verbose_name_plural': 'Telefonick\xe9, p\xedsemn\xe9 a internetov\xe9 p.',
            },
            bases=('services.service',),
        ),
    ]
