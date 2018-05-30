# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.management import update_all_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations


def migrate_therapy(apps, schema_editor):
    update_all_contenttypes(interactive=False)

    ct = ContentType.objects.get_by_natural_key("services", "Therapy")
    ct_wt = ContentType.objects.get_by_natural_key("services", "WorkTherapy")
    ct_wtm = ContentType.objects.get_by_natural_key("services", "WorkTherapyMeeting")
    ct_cw = ContentType.objects.get_by_natural_key("services", "CommunityWork")

    Therapy = apps.get_model("services", "Therapy")
    WorkTherapy = apps.get_model("services", "WorkTherapy")
    WorkTherapyMeeting = apps.get_model("services", "WorkTherapyMeeting")
    CommunityWork = apps.get_model("services", "CommunityWork")

    for service in WorkTherapy.objects.all():
        if service.content_type_id == ct_wt.id:
            s = Therapy()
            s.work_therapy = True
            s.encounter = service.encounter
            s.title = service.title
            s.created = service.created
            s.modified = service.modified
            s.content_type_id = ct.id
            s.save()
            service.delete()
    for service in WorkTherapyMeeting.objects.all():
        if service.content_type_id == ct_wtm.id:
            s = Therapy()
            s.therapy_meeting = True
            s.encounter = service.encounter
            s.title = service.title
            s.created = service.created
            s.modified = service.modified
            s.content_type_id = ct.id
            s.save()
            service.delete()
    for service in CommunityWork.objects.all():
        if service.content_type_id == ct_cw.id:
            s = Therapy()
            s.community_work = True
            s.encounter = service.encounter
            s.title = service.title
            s.created = service.created
            s.modified = service.modified
            s.content_type_id = ct.id
            s.save()
            service.delete()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0028_auto_20180530_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapy',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='services.Service')),
                ('work_therapy', models.BooleanField(default=False, verbose_name='a) Pracovn\xed terapie')),
                ('therapy_meeting', models.BooleanField(default=False, verbose_name='b) Sch\u016fzka pracovn\xed terapie')),
                ('community_work', models.BooleanField(default=False, verbose_name='c) Obecn\u011b prosp\u011b\u0161n\xe9 pr\xe1ce')),
            ],
            options={
                'verbose_name': 'Pracovn\xed terapie (samospr\xe1va)',
                'verbose_name_plural': 'Pracovn\xed terapie (samospr\xe1va)',
            },
            bases=('services.service',),
        ),
        migrations.RunPython(code=migrate_therapy, reverse_code=reverse),
    ]
