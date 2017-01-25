# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20170123_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugusage',
            name='application',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Aplikace', choices=[(1, 'injek\u010dn\u011b do \u017e\xedly'), (2, 'injek\u010dn\u011b do svalu'), (3, '\xfastn\u011b'), (4, 'sniff (\u0161\u0148up\xe1n\xed)'), (5, 'kou\u0159en\xed'), (6, 'inhalace'), (7, 'Nen\xed zn\xe1mo')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='drugusage',
            name='frequency',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u010cetnost', choices=[(1, 'm\xe9n\u011b ne\u017e 3x m\u011bs\xed\u010dn\u011b'), (2, '1x t\xfddn\u011b'), (3, 'v\xedkendov\u011b'), (4, 'obden'), (5, 'denn\u011b'), (6, '2-3x denn\u011b'), (7, 'v\xedce ne\u017e 3x denn\u011b'), (8, 'neu\u017eita d\xe9le ne\u017e 6 m\u011bs\xedc\u016f'), (10, 'neu\u017eita posledn\xed 3 m\u011bs\xedce'), (11, 'neu\u017eita v posledn\xedm m\u011bs\xedci'), (12, 'Nen\xed zn\xe1mo')]),
            preserve_default=True,
        ),
    ]
