# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0029_therapy'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
            ],
            options={
                'abstract': False,
            },
            bases=('services.service',),
        ),
        migrations.DeleteModel(
            name='CommunityWork',
        ),
        migrations.CreateModel(
            name='CommunityWork',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
            ],
            options={
                'abstract': False,
            },
            bases=('services.service',),
        ),
        migrations.DeleteModel(
            name='WorkTherapy',
        ),
        migrations.CreateModel(
            name='WorkTherapy',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
            ],
            options={
                'abstract': False,
            },
            bases=('services.service',),
        ),
        migrations.DeleteModel(
            name='WorkTherapyMeeting',
        ),
        migrations.CreateModel(
            name='WorkTherapyMeeting',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
            ],
            options={
                'abstract': False,
            },
            bases=('services.service',),
        ),
    ]
