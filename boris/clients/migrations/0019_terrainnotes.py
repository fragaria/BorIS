# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0018_auto_20170329_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerrainNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Kdy')),
                ('note', models.TextField(verbose_name='Z\xe1pis', blank=True)),
                ('town', models.ForeignKey(related_name='+', verbose_name='M\u011bsto', to='clients.Town')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Kdo')),
            ],
            options={
                'verbose_name': 'Z\xe1pis z ter\xe9nu',
                'verbose_name_plural': 'Z\xe1pisy z ter\xe9nu',
            },
            bases=(models.Model,),
        ),
    ]
