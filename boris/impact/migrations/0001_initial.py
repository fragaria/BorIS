# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchEncounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_client', models.BooleanField(default=None)),
                ('is_anonymous', models.BooleanField(default=None)),
                ('is_close_person', models.BooleanField(default=None)),
                ('is_sex_partner', models.BooleanField(default=None)),
                ('is_by_phone', models.BooleanField(default=None)),
                ('client_sex', models.PositiveSmallIntegerField()),
                ('primary_drug', models.PositiveSmallIntegerField()),
                ('primary_drug_usage', models.PositiveSmallIntegerField()),
                ('performed_on', models.DateField()),
                ('month', models.SmallIntegerField()),
                ('year', models.SmallIntegerField()),
                ('grouping_constant', models.SmallIntegerField()),
            ],
            options={
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type_model', models.CharField(max_length=255)),
                ('performed_on', models.DateField()),
                ('month', models.SmallIntegerField()),
                ('year', models.SmallIntegerField()),
                ('is_client', models.BooleanField(default=False)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('grouping_constant', models.SmallIntegerField()),
            ],
            options={
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchSyringeCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.SmallIntegerField()),
                ('performed_on', models.DateField()),
                ('month', models.SmallIntegerField()),
                ('year', models.SmallIntegerField()),
                ('grouping_constant', models.SmallIntegerField()),
            ],
            options={
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
