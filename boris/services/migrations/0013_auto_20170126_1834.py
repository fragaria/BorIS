# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_auto_20170126_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrineTest',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('drug_test', models.BooleanField(default=False, verbose_name='a) Test na drogy')),
                ('pregnancy_test', models.BooleanField(default=False, verbose_name='b) T\u011bhotensk\xfd test')),
            ],
            options={
                'verbose_name': 'Orienta\u010dn\xed test z mo\u010di',
                'verbose_name_plural': 'Orienta\u010dn\xed test z mo\u010di',
            },
            bases=('services.service',),
        ),
    ]
