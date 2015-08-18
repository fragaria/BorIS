# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import fragapy.common.models.adminlink


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='N\xe1zev skupiny')),
                ('date', models.DateField(verbose_name='Kdy')),
                ('note', models.TextField(verbose_name='Pozn\xe1mka', blank=True)),
                ('clients', models.ManyToManyField(to='clients.Client', verbose_name='Klienti')),
                ('town', models.ForeignKey(related_name='+', verbose_name='M\u011bsto', to='clients.Town')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Kdo')),
            ],
            options={
                'verbose_name': 'Skupinov\xfd kontakt',
                'verbose_name_plural': 'Skupinov\xe9 kontakty',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
    ]
