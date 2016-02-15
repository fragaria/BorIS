# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20150819_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialwork',
            old_name='socio_legal',
            new_name='social',
        ),
        migrations.AddField(
            model_name='socialwork',
            name='legal',
            field=models.BooleanField(default=False, verbose_name='b) trestn\u011b-pr\xe1vn\xed'),
            preserve_default=True,
        ),
    ]
