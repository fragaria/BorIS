# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import boris.clients.models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_groupcontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=boris.clients.models.get_client_card_filename)),
                ('client', models.ForeignKey(to='clients.Client', to_field=b'client_card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
