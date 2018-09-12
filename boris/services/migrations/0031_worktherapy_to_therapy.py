# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from boris.services.models.core import TimeDotation
from boris.utils.contenttypes import update_all_contenttypes


def add_default_therapy_time(apps, schema_editor):
    TimeDotation = apps.get_model('services', 'TimeDotation')
    Therapy = apps.get_model('services', 'Therapy')
    work_therapy_ct = ContentType.objects.get_by_natural_key("services", "WorkTherapy")
    therapy_ct = ContentType.objects.get_by_natural_key('services', 'Therapy')

    # create ct for IndirectService now (otherwise would be created in post_migrate signal, which is too late)
    update_all_contenttypes(interactive=False)

    wt_td = TimeDotation.objects.get(content_type_id=work_therapy_ct.id)

    print 'Adding dotation for ct: %s' % Therapy._meta.object_name
    t_td, _ = TimeDotation.objects.get_or_create(content_type_id=therapy_ct.id,
                                               default_minutes=wt_td.default_minutes,
                                               defaults={'minutes': wt_td.minutes})


def delete_therapy_timedotations(apps, schema_editor):
    ct = ContentType.objects.get_by_natural_key("services", "WorkTherapy")
    TimeDotation.objects.filter(content_type_id=ct.id).delete()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0030_auto_20180530_1440'),
    ]

    operations = [
        migrations.RunPython(code=add_default_therapy_time, reverse_code=reverse),
        migrations.RunPython(code=delete_therapy_timedotations, reverse_code=reverse),
    ]
