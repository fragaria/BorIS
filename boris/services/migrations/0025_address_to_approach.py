# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.management import update_all_contenttypes

from boris.services.models import Address, Approach
from boris.services.models.core import TimeDotation


def copy_data(apps, schema_editor):
    Address = apps.get_model("services", "Address")
    Approach = apps.get_model("services", "Approach")
    ApproachCount = Approach.objects.all().count()
    ct = ContentType.objects.get_by_natural_key("services", "Approach")
    count = 0
    title = _(u'Oslovení')
    for address in Address.objects.all().order_by('encounter__id').distinct():
        if address.title == title:
            approach = Approach()
            approach.encounter = address.encounter
            approach.title = address.title
            approach.content_type_id = ct.id
            approach.created = address.created
            approach.modified = address.modified
            approach.save()
            count += 1

    print 'Successfully migrated %d services of type Address' % count


def add_default_approach_time(apps, schema_editor):
    TimeDotation = apps.get_model('services', 'TimeDotation')

    # create ct for IndirectService now (otherwise would be created in post_migrate signal, which is too late)
    update_all_contenttypes(interactive=False)

    data = ((apps.get_model('services', 'Approach')), 60)

    print 'Adding dotation for ct: %s' % data[0]._meta.object_name
    ct = ContentType.objects.get_by_natural_key(data[0]._meta.app_label,
                                                data[0]._meta.object_name.lower())
    td, _ = TimeDotation.objects.get_or_create(content_type_id=ct.id,
                                               default_minutes=data[1],
                                               defaults={'minutes': data[1]})

def delete_address_timedotations(apps, schema_editor):
    ct = ContentType.objects.get_by_natural_key("services", "Address")
    TimeDotation.objects.filter(content_type_id=ct.id).delete()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0024_approach'),
    ]

    operations = [
        migrations.RunPython(code=copy_data, reverse_code=reverse),
        migrations.RunPython(code=add_default_approach_time, reverse_code=reverse),
        migrations.RunPython(code=delete_address_timedotations, reverse_code=reverse),
    ]