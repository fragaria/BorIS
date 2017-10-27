# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_encounter_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndirectService',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
            ],
            options={
                'verbose_name': 'Telefonick\xe9, p\xedsemn\xe9 a internetov\xe9 poradenstv\xed',
                'verbose_name_plural': 'Telefonick\xe9, p\xedsemn\xe9 a internetov\xe9 poradenstv\xed',
            },
            bases=('services.service',),
        ),
    ]
