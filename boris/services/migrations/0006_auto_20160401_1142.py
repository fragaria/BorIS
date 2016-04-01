# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fragapy.fields.models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20160323_1416'),
        ('services', '0005_auto_20160323_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='group_contact',
            field=models.ForeignKey(verbose_name='P\u0159idru\u017een\xe1 skupina', blank=True, to='clients.GroupContact', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='utilitywork',
            name='refs',
            field=fragapy.fields.models.MultiSelectField(max_length=40, verbose_name='Odkazy', choices=[(b'fp', '1) Ter\xe9nn\xed programy'), (b'cc', '2) Kontaktn\xed centrum'), (b'mf', '3) Pobytov\xe1 l\xe9\u010dba'), (b'ep', '4) V\xfdm\u011bnn\xfd program'), (b't', '5) Testy'), (b'hs', '6) Zdravotn\xed slu\u017eby'), (b'ss', '7) Soci\xe1ln\xed slu\u017eby'), (b'can', '8) Dohodunt\xfd kontakt neprob\u011bhl / event. p\xe9\u010de ukon\u010dena klientem bez dohody'), (b'sub', '9) Substituce'), (b'amb', '10) Ambulantn\xed l\xe9\u010dba'), (b'o', '10) jin\xe9')]),
            preserve_default=True,
        ),
    ]
