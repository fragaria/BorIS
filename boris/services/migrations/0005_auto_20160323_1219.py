# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fragapy.fields.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_separate_social_and_legal'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ParentAdvisory',
        ),
        migrations.CreateModel(
            name='Breathalyzer',
            fields=[
            ],
            options={
                'verbose_name': 'Alkotester',
                'proxy': True,
                'verbose_name_plural': 'Alkotester',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='FoodService',
            fields=[
            ],
            options={
                'verbose_name': 'Potravinov\xfd servis',
                'proxy': True,
                'verbose_name_plural': 'Potravinov\xfd servis',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='PregnancyTest',
            fields=[
            ],
            options={
                'verbose_name': 'T\u011bhotensk\xfd test',
                'proxy': True,
                'verbose_name_plural': 'T\u011bhotensk\xfd test',
            },
            bases=('services.service',),
        ),
        migrations.AddField(
            model_name='harmreduction',
            name='capsule_count',
            field=models.PositiveIntegerField(default=0, verbose_name='po\u010det vydan\xfdch kapsl\xed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='counselling',
            field=models.BooleanField(default=False, verbose_name='c) p\u0159edl\xe9\u010debn\xe9 indiviu\xe1ln\xed poradenstv\xed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='other',
            field=models.BooleanField(default=False, verbose_name='e) jin\xe1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='service_mediation',
            field=models.BooleanField(default=False, verbose_name='d) zprost\u0159edkov\xe1n\xed dal\u0161\xedch slu\u017eeb'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialwork',
            name='social',
            field=models.BooleanField(default=False, verbose_name='a) soci\xe1ln\xed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='utilitywork',
            name='refs',
            field=fragapy.fields.models.MultiSelectField(max_length=40, verbose_name='Odkazy', choices=[(b'fp', '1) Ter\xe9nn\xed programy'), (b'cc', '2) Kontaktn\xed centrum'), (b'mf', '3) L\xe9\u010debn\xe1 za\u0159\xedzen\xed'), (b'ep', '4) V\xfdm\u011bnn\xfd program'), (b't', '5) Testy'), (b'hs', '6) Zdravotn\xed slu\u017eby'), (b'ss', '7) Soci\xe1ln\xed slu\u017eby'), (b'can', '8) Dohodunt\xfd kontakt neprob\u011bhl / event. p\xe9\u010de ukon\u010dena klientem bez dohody'), (b'sub', '9) Substituce'), (b'o', '10) jin\xe9')]),
            preserve_default=True,
        ),
    ]
