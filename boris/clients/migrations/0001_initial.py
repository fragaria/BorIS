# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import model_utils.fields
import fragapy.common.models.adminlink
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anamnesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('filled_when', models.DateField(verbose_name='Datum kontaktu')),
                ('nationality', models.PositiveSmallIntegerField(default=4, verbose_name='St\xe1tn\xed p\u0159\xedslu\u0161nost', choices=[(1, '\u010cesk\xe1 republika'), (2, 'Jin\xe9 - EU'), (3, 'Jin\xe9 - non-EU'), (4, 'Nezn\xe1mo')])),
                ('ethnic_origin', models.PositiveSmallIntegerField(default=3, verbose_name='Etnick\xe1 p\u0159\xedslu\u0161nost', choices=[(1, 'Ne-romsk\xe1'), (2, 'Romsk\xe1'), (3, 'Nesledov\xe1no')])),
                ('living_condition', models.PositiveSmallIntegerField(default=7, verbose_name='Bydlen\xed (s k\xfdm klient \u017eije)', choices=[(1, 'S\xe1m'), (2, 'S rodi\u010di/rodinou'), (3, 'S p\u0159\xe1teli'), (4, 'S partnerem'), (5, 'S partnerem a d\xedt\u011btem'), (6, 'S\xe1m s d\xedt\u011btem'), (7, 'Nen\xed zn\xe1mo')])),
                ('accomodation', models.PositiveSmallIntegerField(default=8, verbose_name='Bydlen\xed (kde klient \u017eije)', choices=[(1, 'Doma (u rodi\u010d\u016f)'), (2, 'Vlastn\xed byt (i pronajat\xfd)'), (3, 'Ciz\xed byt'), (4, 'Ubytovna'), (5, 'Squat'), (6, 'Kas\xe1rna'), (7, 'Bez domova, na ulici'), (8, 'Nen\xed zn\xe1mo')])),
                ('lives_with_junkies', models.NullBooleanField(verbose_name='\u017dije klient s osobou u\u017e\xedvaj\xedc\xed drogy?')),
                ('employment', models.PositiveSmallIntegerField(default=8, verbose_name='Zam\u011bstn\xe1n\xed / \u0161kola', choices=[(1, 'Pravideln\xe9 zam.'), (2, '\u0160kola'), (3, 'P\u0159\xedle\u017eitostn\xe1 pr\xe1ce'), (4, 'Registrov\xe1n na \xdaP'), (5, 'Bez zam\u011bstn\xe1n\xed'), (6, 'D\xe1vky SZ'), (8, 'Nen\xed zn\xe1mo')])),
                ('education', models.PositiveSmallIntegerField(default=7, verbose_name='Vzd\u011bl\xe1n\xed', choices=[(1, 'Z\xe1kladn\xed'), (2, 'Vyu\u010den'), (3, 'St\u0159edn\xed s maturitou'), (4, 'Vy\u0161\u0161\xed odborn\xe9'), (5, 'Vysoko\u0161kolsk\xe9'), (6, 'Neukon\u010den\xe9 z\xe1kladn\xed'), (7, 'Nen\xed zn\xe1mo')])),
                ('been_cured_before', models.BooleanField(default=None, verbose_name='D\u0159\xedve l\xe9\u010den')),
                ('been_cured_currently', models.BooleanField(default=None, verbose_name='Nyn\xed l\xe9\u010den')),
                ('author', models.ForeignKey(verbose_name='Vyplnil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Anamn\xe9za',
                'verbose_name_plural': 'Anamn\xe9zy',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='ClientNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Datum a \u010das')),
                ('text', models.TextField(verbose_name='Text')),
                ('author', models.ForeignKey(related_name='notes_added', verbose_name='Autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime', '-id'),
                'verbose_name': 'Pozn\xe1mka',
                'verbose_name_plural': 'Pozn\xe1mky',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiseaseTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disease', models.PositiveSmallIntegerField(verbose_name='Testovan\xe9 onemocn\u011bn\xed', choices=[(1, 'HIV'), (2, 'VHA'), (3, 'VHB'), (4, 'VHC'), (5, 'Syfilis')])),
                ('result', models.SmallIntegerField(default=0, verbose_name='V\xfdsledek testu', choices=[(0, 'Nezn\xe1mo, zda testov\xe1n'), (1, 'Testov\xe1n - pozitivn\xed'), (2, 'Testov\xe1n - negativn\xed'), (3, 'Testov\xe1n - v\xfdsledek nezn\xe1m\xfd'), (4, 'Nikdy netestov\xe1n'), (5, 'Nevyzvedl v\xfdsledek')])),
                ('anamnesis', models.ForeignKey(to='clients.Anamnesis')),
            ],
            options={
                'verbose_name': 'Vy\u0161et\u0159en\xed onemocn\u011bn\xed',
                'verbose_name_plural': 'Vy\u0161et\u0159en\xed onemocn\u011bn\xed',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='N\xe1zev', db_index=True)),
            ],
            options={
                'verbose_name': 'Okres',
                'verbose_name_plural': 'Okresy',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='DrugUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drug', models.PositiveSmallIntegerField(verbose_name='Droga', choices=[(3, 'Pervitin, jin\xe9 amfetaminy'), (4, 'Subutex, Ravata, Buprenorphine alkaloid - leg\xe1ln\u011b'), (5, 'Tab\xe1k'), (8, 'THC'), (9, 'Ext\xe1ze'), (10, 'Designer drugs'), (11, 'Heroin'), (12, 'Braun a jin\xe9 opi\xe1ty'), (13, 'Surov\xe9 opium'), (14, 'Subutex, Ravata, Buprenorphine alkaloid - ileg\xe1ln\u011b'), (16, 'Alkohol'), (17, 'Inhala\u010dn\xed l\xe1tky, \u0159edidla'), (18, 'Medikamenty'), (19, 'Metadon'), (20, 'Kokain, crack'), (21, 'Suboxone'), (22, 'Vendal'), (23, 'LSD'), (24, 'Lysohl\xe1vky'), (25, 'Nezn\xe1mo')])),
                ('application', models.PositiveSmallIntegerField(verbose_name='Aplikace', choices=[(1, 'injek\u010dn\u011b do \u017e\xedly'), (2, 'injek\u010dn\u011b do svalu'), (3, '\xfastn\u011b'), (4, 'sniff (\u0161\u0148up\xe1n\xed)'), (5, 'kou\u0159en\xed'), (6, 'inhalace'), (7, 'Nen\xed zn\xe1mo')])),
                ('frequency', models.PositiveSmallIntegerField(verbose_name='\u010cetnost', choices=[(1, 'm\xe9n\u011b ne\u017e 3x m\u011bs\xed\u010dn\u011b'), (2, '1x t\xfddn\u011b'), (3, 'v\xedkendov\u011b'), (4, 'obden'), (5, 'denn\u011b'), (6, '2-3x denn\u011b'), (7, 'v\xedce ne\u017e 3x denn\u011b'), (8, 'neu\u017eita d\xe9le ne\u017e 6 m\u011bs\xedc\u016f'), (10, 'neu\u017eita posledn\xed 3 m\u011bs\xedce'), (11, 'neu\u017eita v posledn\xedm m\u011bs\xedci'), (12, 'Nen\xed zn\xe1mo')])),
                ('first_try_age', models.PositiveSmallIntegerField(verbose_name='Prvn\xed u\u017eit\xed (v\u011bk)')),
                ('first_try_iv_age', models.PositiveSmallIntegerField(null=True, verbose_name='Prvn\xed i.v. u\u017eit\xed (v\u011bk)', blank=True)),
                ('first_try_application', models.PositiveSmallIntegerField(verbose_name='Zp\u016fsob prvn\xedho u\u017eit\xed', choices=[(1, 'injek\u010dn\u011b do \u017e\xedly'), (2, 'injek\u010dn\u011b do svalu'), (3, '\xfastn\u011b'), (4, 'sniff (\u0161\u0148up\xe1n\xed)'), (5, 'kou\u0159en\xed'), (6, 'inhalace'), (7, 'Nen\xed zn\xe1mo')])),
                ('was_first_illegal', models.NullBooleanField(verbose_name='Prvn\xed neleg. droga')),
                ('is_primary', models.BooleanField(default=None, verbose_name='Prim\xe1rn\xed droga')),
                ('note', models.TextField(null=True, verbose_name='Pozn\xe1mka', blank=True)),
                ('anamnesis', models.ForeignKey(verbose_name='Anamn\xe9za', to='clients.Anamnesis')),
            ],
            options={
                'verbose_name': 'U\u017e\xedvan\xe1 droga',
                'verbose_name_plural': 'U\u017e\xedvan\xe9 drogy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(verbose_name='N\xe1zev', max_length=255, editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Osoba',
                'verbose_name_plural': 'Osoby',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='clients.Person')),
                ('code', models.CharField(unique=True, max_length=63, verbose_name='K\xf3d')),
                ('sex', models.PositiveSmallIntegerField(verbose_name='Pohlav\xed', choices=[(1, '\u017eena'), (2, 'mu\u017e')])),
                ('first_name', models.CharField(max_length=63, null=True, verbose_name='Jm\xe9no', blank=True)),
                ('last_name', models.CharField(max_length=63, null=True, verbose_name='P\u0159\xedjmen\xed', blank=True)),
                ('birthdate', models.DateField(help_text='Pokud zn\xe1te pouze rok, za\u0161krtn\u011bte pol\xed\u010dko `Zn\xe1m\xfd pouze rok`.', null=True, verbose_name='Datum narozen\xed', blank=True)),
                ('birthdate_year_only', models.BooleanField(default=False, verbose_name='Zn\xe1m\xfd pouze rok')),
                ('primary_drug', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Prim\xe1rn\xed droga', choices=[(3, 'Pervitin, jin\xe9 amfetaminy'), (4, 'Subutex, Ravata, Buprenorphine alkaloid - leg\xe1ln\u011b'), (5, 'Tab\xe1k'), (8, 'THC'), (9, 'Ext\xe1ze'), (10, 'Designer drugs'), (11, 'Heroin'), (12, 'Braun a jin\xe9 opi\xe1ty'), (13, 'Surov\xe9 opium'), (14, 'Subutex, Ravata, Buprenorphine alkaloid - ileg\xe1ln\u011b'), (16, 'Alkohol'), (17, 'Inhala\u010dn\xed l\xe1tky, \u0159edidla'), (18, 'Medikamenty'), (19, 'Metadon'), (20, 'Kokain, crack'), (21, 'Suboxone'), (22, 'Vendal'), (23, 'LSD'), (24, 'Lysohl\xe1vky'), (25, 'Nezn\xe1mo')])),
                ('primary_drug_usage', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Zp\u016fsob aplikace', choices=[(1, 'injek\u010dn\u011b do \u017e\xedly'), (2, 'injek\u010dn\u011b do svalu'), (3, '\xfastn\u011b'), (4, 'sniff (\u0161\u0148up\xe1n\xed)'), (5, 'kou\u0159en\xed'), (6, 'inhalace'), (7, 'Nen\xed zn\xe1mo')])),
                ('close_person', models.BooleanField(default=False, verbose_name='Osoba bl\xedzk\xe1 (rodi\u010de apod.)')),
                ('sex_partner', models.BooleanField(default=False, verbose_name='Sexu\xe1ln\xed partner')),
            ],
            options={
                'verbose_name': 'Klient',
                'verbose_name_plural': 'Klienti',
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Anonymous',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='clients.Person')),
                ('drug_user_type', models.PositiveSmallIntegerField(verbose_name='Typ', choices=[(1, 'neu\u017eivatel'), (2, 'neIV'), (3, 'IV'), (4, 'rodi\u010d')])),
                ('sex', models.PositiveSmallIntegerField(verbose_name='Pohlav\xed', choices=[(1, '\u017eena'), (2, 'mu\u017e')])),
            ],
            options={
                'verbose_name': 'Anonym',
                'verbose_name_plural': 'Anonymov\xe9',
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='PractitionerContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_or_institution', models.CharField(max_length=255, verbose_name='Osoba nebo instituce')),
                ('date', models.DateField(verbose_name='Kdy')),
                ('note', models.TextField(verbose_name='Pozn\xe1mka', blank=True)),
            ],
            options={
                'verbose_name': 'Odborn\xfd kontakt',
                'verbose_name_plural': 'Odborn\xe9 kontakty',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='N\xe1zev', db_index=True)),
            ],
            options={
                'verbose_name': 'Kraj',
                'verbose_name_plural': 'Kraje',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.CreateModel(
            name='RiskyManners',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('behavior', models.PositiveIntegerField(choices=[(1, 'Sd\xedlen\xed n\xe1\u010din\xed'), (2, 'Nechr\xe1n\u011bn\xfd sex'), (3, 'Sd\xedlen\xed jehel'), (4, 'Nitro\u017eiln\xed aplikace'), (5, 'Rizikov\xe1 aplikace'), (6, 'P\u0159ed\xe1vkov\xe1n\xed'), (7, 'Zdravotn\xed komplikace')])),
                ('periodicity_in_past', models.PositiveIntegerField(blank=True, null=True, verbose_name='Jak \u010dasto v minulosti', choices=[(1, 'Nikdy'), (2, 'Jednor\xe1zov\u011b'), (3, 'Opakovan\u011b '), (4, 'Nen\xed zn\xe1mo')])),
                ('periodicity_in_present', models.PositiveIntegerField(blank=True, null=True, verbose_name='Jak \u010dasto v p\u0159\xedtomnosti', choices=[(1, 'Nikdy'), (2, 'Jednor\xe1zov\u011b'), (3, 'Opakovan\u011b '), (4, 'Nen\xed zn\xe1mo')])),
                ('anamnesis', models.ForeignKey(verbose_name='Anamn\xe9za', to='clients.Anamnesis')),
            ],
            options={
                'verbose_name': 'Rizikov\xe9 chov\xe1n\xed',
                'verbose_name_plural': 'Rizikov\xe1 chov\xe1n\xed',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='N\xe1zev', db_index=True)),
                ('district', models.ForeignKey(verbose_name='Okres', to='clients.District')),
            ],
            options={
                'verbose_name': 'M\u011bsto',
                'verbose_name_plural': 'M\u011bsta',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.AlterUniqueTogether(
            name='riskymanners',
            unique_together=set([('behavior', 'anamnesis')]),
        ),
        migrations.AddField(
            model_name='practitionercontact',
            name='town',
            field=models.ForeignKey(related_name='+', verbose_name='M\u011bsto', to='clients.Town'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practitionercontact',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Kdo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='content_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='drugusage',
            unique_together=set([('drug', 'anamnesis')]),
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(verbose_name='Kraj', to='clients.Region'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='diseasetest',
            unique_together=set([('disease', 'anamnesis')]),
        ),
        migrations.AddField(
            model_name='clientnote',
            name='client',
            field=models.ForeignKey(related_name='notes', verbose_name='Klient', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='town',
            field=models.ForeignKey(verbose_name='M\u011bsto', to='clients.Town'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='anonymous',
            unique_together=set([('sex', 'drug_user_type')]),
        ),
        migrations.AddField(
            model_name='anamnesis',
            name='client',
            field=models.OneToOneField(verbose_name='Klient', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anamnesis',
            name='filled_where',
            field=models.ForeignKey(verbose_name='M\u011bsto kontaktu', to='clients.Town'),
            preserve_default=True,
        ),
    ]
