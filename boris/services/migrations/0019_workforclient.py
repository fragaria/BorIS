# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0018_delete_pregnancytest'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkForClient',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('contact_institution', models.BooleanField(default=False, verbose_name='a) kontakt s institucemi')),
                ('message', models.BooleanField(default=False, verbose_name='b) zpr\xe1va, doporu\u010den\xed')),
                ('search_information', models.BooleanField(default=False, verbose_name='c) vyhled\xe1v\xe1n\xed a zji\u0161\u0165ov\xe1n\xed informac\xed pro klienta')),
                ('case_conference', models.BooleanField(default=False, verbose_name='d) p\u0159\xedpadov\xe1 konference')),
            ],
            options={
                'verbose_name': 'Pr\xe1ce ve prosp\u011bch klienta',
                'verbose_name_plural': 'Pr\xe1ce ve prosp\u011bch klienta',
            },
            bases=('services.service',),
        ),
    ]
