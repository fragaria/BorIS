# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.management import update_all_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations
import fragapy.common.models.adminlink


def add_default_times(apps, schema_editor):
    TimeDotation = apps.get_model('services', 'TimeDotation')

    # create ct for IndirectService now (otherwise would be created in post_migrate signal, which is too late)
    update_all_contenttypes(interactive=False)

    DATA = [
        ((apps.get_model('services', 'Address')), 60),
        ((apps.get_model('services', 'Approach')), 60),
        ((apps.get_model('services', 'ContactWork')), 10),
        ((apps.get_model('services', 'IncomeFormFillup')), 60),
        ((apps.get_model('services', 'IndividualCounselling')), 30),
        ((apps.get_model('services', 'GroupCounselling')), 120),
        ((apps.get_model('services', 'CrisisIntervention')), 30),
        ((apps.get_model('services', 'WorkTherapy')), 60),
        ((apps.get_model('services', 'SocialWork')), 30),
        ((apps.get_model('services', 'UtilityWork')), 30),
        ((apps.get_model('services', 'AsistService')), 30),
        ((apps.get_model('services', 'WorkWithFamily')), 30),
        ((apps.get_model('services', 'BasicMedicalTreatment')), 10),
        ((apps.get_model('services', 'PostUsage')), 20),
        ((apps.get_model('services', 'InformationService')), 5),
        ((apps.get_model('services', 'HarmReduction')), 5),
        ((apps.get_model('services', 'HygienicService')), 20),
        ((apps.get_model('services', 'FoodService')), 20),
        ((apps.get_model('services', 'DiseaseTest')), 30),
        ((apps.get_model('services', 'UrineTest')), 20),
        ((apps.get_model('services', 'IndirectService')), 10),
    ]
    for data in DATA:
        print 'Adding dotation for ct: %s' % data[0]._meta.object_name
        ct = ContentType.objects.get_by_natural_key(data[0]._meta.app_label,
                                                    data[0]._meta.object_name.lower())
        td, _ = TimeDotation.objects.get_or_create(content_type_id=ct.id,
                                                   default_minutes=data[1],
                                                   defaults={'minutes': data[1]})


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('services', '0021_indirectservice'),
    ]

    operations = [
        # migrations.DeleteModel(name='TimeDotation'),
        # migrations.DeleteModel((apps.get_model('services', 'TimeDotation'))),
        migrations.CreateModel(
            name='TimeDotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minutes', models.PositiveIntegerField(verbose_name='Po\u010det minut')),
                ('default_minutes', models.PositiveIntegerField(verbose_name='V\xfdchoz\xed po\u010det minut', editable=False)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', verbose_name='Typ slu\u017eby')),
            ],
            options={
                'verbose_name': '\u010casov\xe1 dotace',
                'verbose_name_plural': '\u010casov\xe9 dotace',
            },
            bases=(models.Model, fragapy.common.models.adminlink.AdminLinkMixin),
        ),
        migrations.RunPython(code=add_default_times, reverse_code=reverse)
    ]
