# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import fragapy.common.models.adminlink


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0024_auto_20180716_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyringeCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(verbose_name='how much')),
                ('date', models.DateField(verbose_name='when')),
                ('location', models.CharField(max_length=255, verbose_name='location', blank=True)),
                ('persons', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='who')),
                ('town', models.ForeignKey(related_name='+', verbose_name='town', to='clients.Town')),
            ],
            options={
                'verbose_name': 'syringe collection',
                'verbose_name_plural': 'syringe collections',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
    ]
