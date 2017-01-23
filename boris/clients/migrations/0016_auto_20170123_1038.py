# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20170119_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='primary_drug',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Prim\xe1rn\xed droga', choices=[(3, 'Pervitin, jin\xe9 amfetaminy'), (4, 'Subutex, Ravata, Buprenorphine alkaloid - leg\xe1ln\u011b'), (5, 'Tab\xe1k'), (8, 'THC'), (9, 'Ext\xe1ze'), (10, 'Designer drugs'), (11, 'Heroin'), (12, 'Braun a jin\xe9 opi\xe1ty'), (13, 'Surov\xe9 opium'), (14, 'Subutex, Ravata, Buprenorphine alkaloid - ileg\xe1ln\u011b'), (16, 'Alkohol'), (17, 'Inhala\u010dn\xed l\xe1tky, \u0159edidla'), (18, 'Medikamenty'), (19, 'Metadon'), (20, 'Kokain, crack'), (21, 'Suboxone'), (22, 'Vendal'), (23, 'LSD'), (24, 'Lysohl\xe1vky'), (25, 'Nezn\xe1mo'), (26, 'Patologick\xe9 hr\xe1\u010dstv\xed'), (27, 'Jin\xe1 nel\xe1tkov\xe1 z\xe1vislost')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='drugusage',
            name='drug',
            field=models.PositiveSmallIntegerField(verbose_name='Droga', choices=[(3, 'Pervitin, jin\xe9 amfetaminy'), (4, 'Subutex, Ravata, Buprenorphine alkaloid - leg\xe1ln\u011b'), (5, 'Tab\xe1k'), (8, 'THC'), (9, 'Ext\xe1ze'), (10, 'Designer drugs'), (11, 'Heroin'), (12, 'Braun a jin\xe9 opi\xe1ty'), (13, 'Surov\xe9 opium'), (14, 'Subutex, Ravata, Buprenorphine alkaloid - ileg\xe1ln\u011b'), (16, 'Alkohol'), (17, 'Inhala\u010dn\xed l\xe1tky, \u0159edidla'), (18, 'Medikamenty'), (19, 'Metadon'), (20, 'Kokain, crack'), (21, 'Suboxone'), (22, 'Vendal'), (23, 'LSD'), (24, 'Lysohl\xe1vky'), (25, 'Nezn\xe1mo'), (26, 'Patologick\xe9 hr\xe1\u010dstv\xed'), (27, 'Jin\xe1 nel\xe1tkov\xe1 z\xe1vislost')]),
            preserve_default=True,
        ),
    ]
