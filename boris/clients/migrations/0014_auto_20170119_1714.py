# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_auto_20161104_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugusage',
            name='first_try_age',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Prvn\xed u\u017eit\xed (v\u011bk)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='drugusage',
            name='first_try_application',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Zp\u016fsob prvn\xedho u\u017eit\xed', choices=[(1, 'injek\u010dn\u011b do \u017e\xedly'), (2, 'injek\u010dn\u011b do svalu'), (3, '\xfastn\u011b'), (4, 'sniff (\u0161\u0148up\xe1n\xed)'), (5, 'kou\u0159en\xed'), (6, 'inhalace'), (7, 'Nen\xed zn\xe1mo')]),
            preserve_default=True,
        ),
    ]
