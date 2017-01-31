# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_auto_20170126_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualCounselling',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('general', models.BooleanField(default=False, verbose_name='a) obecn\xe9')),
                ('structured', models.BooleanField(default=False, verbose_name='b) strukturovan\xe9')),
                ('pre_treatment', models.BooleanField(default=False, verbose_name='c) p\u0159edl\xe9\u010debn\xe9 poradenstv\xed')),
                ('guarantee_interview', models.BooleanField(default=False, verbose_name='d) garantsk\xfd pohovor')),
                ('advice_to_parents', models.BooleanField(default=False, verbose_name='e) poradenstv\xed pro rodi\u010de/osoby bl\xedzk\xe9')),
            ],
            options={
                'verbose_name': 'Individu\xe1ln\xed poradenstv\xed',
                'verbose_name_plural': 'Individu\xe1ln\xed poradenstv\xed',
            },
            bases=('services.service',),
        ),
    ]
