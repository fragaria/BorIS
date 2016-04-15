# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fragapy.common.models.adminlink


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20160323_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='N\xe1zev', db_index=True)),
                ('key', models.SmallIntegerField(verbose_name='K\xf3d')),
            ],
            options={
                'verbose_name': 'Typ skupiny',
                'verbose_name_plural': 'Typy skupin',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.AddField(
            model_name='groupcontact',
            name='type',
            field=models.ForeignKey(related_name='+', default=1, verbose_name='Typ', to='clients.GroupContactType'),
            preserve_default=True,
        ),
    ]
