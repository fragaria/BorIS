# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import fragapy.fields.models
import fragapy.common.models.adminlink
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('performed_on', models.DateField(default=datetime.date.today, verbose_name='Kdy')),
                ('is_by_phone', models.BooleanField(default=False, verbose_name='Telefonick\xfd kontakt')),
                ('performed_by', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Kdo')),
                ('person', models.ForeignKey(related_name='encounters', verbose_name='Osoba', to='clients.Person')),
                ('where', models.ForeignKey(verbose_name='Kde', to='clients.Town')),
            ],
            options={
                'ordering': ('-performed_on',),
                'verbose_name': 'Kontakt',
                'verbose_name_plural': 'Kontakty',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(verbose_name='N\xe1zev', max_length=255, editable=False)),
            ],
            options={
                'ordering': ('encounter',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InformationService',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('safe_usage', models.BooleanField(default=False, verbose_name='1) bezpe\u010dn\xe9 u\u017e\xedv\xe1n\xed')),
                ('safe_sex', models.BooleanField(default=False, verbose_name='2) bezpe\u010dn\xfd sex')),
                ('medical', models.BooleanField(default=False, verbose_name='3) zdravotn\xed')),
                ('socio_legal', models.BooleanField(default=False, verbose_name='4) soci\xe1ln\u011b-pr\xe1vn\xed')),
                ('cure_possibilities', models.BooleanField(default=False, verbose_name='5) mo\u017enosti l\xe9\u010dby')),
                ('literature', models.BooleanField(default=False, verbose_name='6) ti\u0161t\u011bn\xfd informa\u010dn\xed materi\xe1l')),
                ('other', models.BooleanField(default=False, verbose_name='7) ostatn\xed')),
            ],
            options={
                'verbose_name': 'Informa\u010dn\xed servis',
                'verbose_name_plural': 'Informa\u010dn\xed servis',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='HarmReduction',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('in_count', models.PositiveSmallIntegerField(default=0, verbose_name='IN')),
                ('out_count', models.PositiveSmallIntegerField(default=0, verbose_name='OUT')),
                ('svip_person_count', models.PositiveSmallIntegerField(default=0, verbose_name='po\u010det osob ve SVIP')),
                ('standard', models.BooleanField(default=False, help_text='steriln\xed voda, filtry, alkoholov\xe9 tampony', verbose_name='1) standard')),
                ('acid', models.BooleanField(default=False, verbose_name='3) kyselina')),
                ('alternatives', models.BooleanField(default=False, help_text='alobal, kapsle, \u0161\u0148up\xe1tka', verbose_name='2) alternativy')),
                ('condoms', models.BooleanField(default=False, verbose_name='4) prezervativy')),
                ('stericup', models.BooleanField(default=False, verbose_name='5) St\xe9ri-cup/filt')),
                ('other', models.BooleanField(default=False, verbose_name='6) jin\xfd materi\xe1l')),
                ('pregnancy_test', models.BooleanField(default=False, verbose_name='7) t\u011bhotensk\xfd test')),
                ('medical_supplies', models.BooleanField(default=False, help_text='masti, n\xe1plasti, buni\u010dina, vitam\xedny, \u0161krtidlo...', verbose_name='8) zdravotn\xed')),
            ],
            options={
                'verbose_name': 'Harm Reduction',
                'verbose_name_plural': 'Harm Reduction',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='DiseaseTest',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('disease', models.PositiveSmallIntegerField(default=1, verbose_name='Testovan\xe9 onemocn\u011bn\xed', choices=[(1, 'HIV'), (2, 'VHA'), (3, 'VHB'), (4, 'VHC'), (5, 'Syfilis')])),
                ('sign', models.CharField(default=b'i', max_length=1, verbose_name='Stav', choices=[(b'p', 'Pozitivn\xed'), (b'n', 'Negativn\xed'), (b'r', 'Reaktivn\xed'), (b'i', 'Test nepr\u016fkazn\xfd')])),
            ],
            options={
                'verbose_name': 'Testov\xe1n\xed infek\u010dn\xedch nemoc\xed',
                'verbose_name_plural': 'Testov\xe1n\xed infek\u010dn\xedch nemoc\xed',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='AsistService',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('where', fragapy.fields.models.MultiSelectField(max_length=10, verbose_name='Kam', choices=[(b'm', 'zdravotn\xed'), (b's', 'soci\xe1ln\xed'), (b'f', 'l\xe9\u010debn\xe9 za\u0159\xedzen\xed'), (b'o', 'jin\xe9')])),
                ('note', models.TextField(null=True, verbose_name='Pozn\xe1mka', blank=True)),
            ],
            options={
                'verbose_name': 'Doprovod klienta',
                'verbose_name_plural': 'Doprovod klient\u016f',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='SocialWork',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('socio_legal', models.BooleanField(default=False, verbose_name='a) soci\xe1ln\u011b-pr\xe1vn\xed')),
                ('counselling', models.BooleanField(default=False, verbose_name='b) p\u0159edl\xe9\u010debn\xe9 indiviu\xe1ln\xed poradenstv\xed')),
                ('service_mediation', models.BooleanField(default=False, verbose_name='c) zprost\u0159edkov\xe1n\xed dal\u0161\xedch slu\u017eeb')),
                ('other', models.BooleanField(default=False, verbose_name='d) jin\xe1')),
            ],
            options={
                'verbose_name': 'P\u0159\xedpadov\xe1 pr\xe1ce',
                'verbose_name_plural': 'P\u0159\xedpadov\xe9 pr\xe1ce',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='UtilityWork',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('refs', fragapy.fields.models.MultiSelectField(max_length=40, verbose_name='Odkazy', choices=[(b'fp', '1) Terenn\xed programy'), (b'cc', '2) Kontaktn\xed centrum'), (b'mf', '3) L\xe9\u010debn\xe1 za\u0159\xedzen\xed'), (b'ep', '4) V\xfdm\u011bnn\xfd pogram'), (b't', '5) Testy'), (b'hs', '6) Zdravotn\xed slu\u017eby'), (b'ss', '7) Soci\xe1ln\xed slu\u017eby'), (b'can', '8) Dohodunt\xfd kontakt neprob\u011bhl / event. p\xe9\u010de ukon\u010dena klientem bez dohody'), (b'o', '9) jin\xe9')])),
            ],
            options={
                'verbose_name': 'Odkazy',
                'verbose_name_plural': 'Odkazy',
            },
            bases=('services.service',),
        ),
        migrations.AddField(
            model_name='service',
            name='content_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='encounter',
            field=models.ForeignKey(related_name='services', verbose_name='Kontakt', to='services.Encounter'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
            ],
            options={
                'verbose_name': 'Osloven\xed',
                'proxy': True,
                'verbose_name_plural': 'Osloven\xed',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='BasicMedicalTreatment',
            fields=[
            ],
            options={
                'verbose_name': 'Z\xe1kladn\xed zdravotn\xed o\u0161et\u0159en\xed',
                'proxy': True,
                'verbose_name_plural': 'Z\xe1kladn\xed zdravotn\xed o\u0161et\u0159en\xed',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='ContactWork',
            fields=[
            ],
            options={
                'verbose_name': 'Kontaktn\xed pr\xe1ce',
                'proxy': True,
                'verbose_name_plural': 'Kontaktn\xed pr\xe1ce',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='CrisisIntervention',
            fields=[
            ],
            options={
                'verbose_name': 'Pomoc v krizi',
                'proxy': True,
                'verbose_name_plural': 'Pomoci v krizi',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='IncomeExamination',
            fields=[
            ],
            options={
                'verbose_name': 'Prvn\xed kontakt',
                'proxy': True,
                'verbose_name_plural': 'Prvn\xed kontakty',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='IncomeFormFillup',
            fields=[
            ],
            options={
                'verbose_name': 'Vypln\u011bn\xed IN-COME dotazn\xedku',
                'proxy': True,
                'verbose_name_plural': 'Vypln\u011bn\xed IN-COME dotazn\xedk\u016f',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='IndividualCounseling',
            fields=[
            ],
            options={
                'verbose_name': 'Z\xe1kladn\xed poradenstv\xed',
                'proxy': True,
                'verbose_name_plural': 'Z\xe1kladn\xed poradenstv\xed',
            },
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='PhoneUsage',
            fields=[
            ],
            options={
                'verbose_name': 'Pou\u017eit\xed telefonu klientem',
                'proxy': True,
                'verbose_name_plural': 'Pou\u017eit\xed telefonu klientem',
            },
            bases=('services.service',),
        ),
    ]
