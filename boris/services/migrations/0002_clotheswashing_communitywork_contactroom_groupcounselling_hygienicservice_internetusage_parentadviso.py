# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothesWashing',
            fields=[
            ],
            options={
                'verbose_name': 'Pran\xed pr\xe1dla',
                'proxy': True,
                'verbose_name_plural': 'Pran\xed pr\xe1dla',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='CommunityWork',
            fields=[
            ],
            options={
                'verbose_name': 'Obecn\u011b prosp\u011b\u0161n\xe9 pr\xe1ce',
                'proxy': True,
                'verbose_name_plural': 'Obecn\u011b prosp\u011b\u0161n\xe9 pr\xe1ce',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='ContactRoom',
            fields=[
            ],
            options={
                'verbose_name': 'Kontaktn\xed m\xedstnost',
                'proxy': True,
                'verbose_name_plural': 'Kontaktn\xed m\xedstnosti',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='GroupCounselling',
            fields=[
            ],
            options={
                'verbose_name': 'Skupinov\xe9 poradenstv\xed',
                'proxy': True,
                'verbose_name_plural': 'Skupinov\xe1 poradenstv\xed',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='HygienicService',
            fields=[
            ],
            options={
                'verbose_name': 'Hygienick\xfd servis',
                'proxy': True,
                'verbose_name_plural': 'Hygienick\xe9 servisy',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='InternetUsage',
            fields=[
            ],
            options={
                'verbose_name': 'Pou\u017eit\xed internetu klientem',
                'proxy': True,
                'verbose_name_plural': 'Pou\u017eit\xed internetu klientem',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='ParentAdvisory',
            fields=[
            ],
            options={
                'verbose_name': 'Poradenstv\xed pro rodi\u010de',
                'proxy': True,
                'verbose_name_plural': 'Poradenstv\xed pro rodi\u010de',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='PostUsage',
            fields=[
            ],
            options={
                'verbose_name': 'Po\u0161ta',
                'proxy': True,
                'verbose_name_plural': 'Po\u0161ty',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='SocialServicesAgreement',
            fields=[
            ],
            options={
                'verbose_name': 'Uzav\u0159en\xed dohody o poskyt. soc. slu\u017eeb',
                'proxy': True,
                'verbose_name_plural': 'Uzav\u0159en\xed dohod o poskyt. soc. slu\u017eeb',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='WorkTherapy',
            fields=[
            ],
            options={
                'verbose_name': 'Pracovn\xed terapie (samospr\xe1va)',
                'proxy': True,
                'verbose_name_plural': 'Pracovn\xed terapie (samospr\xe1va)',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='WorkTherapyMeeting',
            fields=[
            ],
            options={
                'verbose_name': 'Sch\u016fzka pracovn\xed terapie (samospr\xe1vy)',
                'proxy': True,
                'verbose_name_plural': 'Sch\u016fzka pracovn\xed terapie (samospr\xe1vy)',
            },
            bases=('services.service',),
        ),
    ]
