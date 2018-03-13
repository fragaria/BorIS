# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0023_auto_20171027_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approach',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('number_of_addressed', models.PositiveIntegerField(default=1, verbose_name='1) Po\u010det osloven\xfdch')),
            ],
            options={
                'verbose_name': 'Osloven\xed',
                'verbose_name_plural': 'Osloven\xed',
            },
            bases=('services.service',),
        ),
    ]
