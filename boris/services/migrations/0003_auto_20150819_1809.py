# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_clotheswashing_communitywork_contactroom_groupcounselling_hygienicservice_internetusage_parentadviso'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClothesWashing',
        ),
        migrations.DeleteModel(
            name='HygienicService',
        ),
        migrations.CreateModel(
            name='HygienicService',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('clothing_wash', models.BooleanField(default=False, verbose_name='1) pran\xed pr\xe1dla')),
                ('shower', models.BooleanField(default=False, verbose_name='2) sprcha')),
                ('social_clothing', models.BooleanField(default=False, verbose_name='3) soci\xe1ln\xed \u0161atn\xedk')),
            ],
            options={
                'verbose_name': 'Hygienick\xfd servis',
                'verbose_name_plural': 'Hygienick\xe9 servisy',
            },
            bases=('services.service',),
        ),
    ]
