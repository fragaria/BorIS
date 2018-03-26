# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from boris.services.models import Address, Approach

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


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0024_approach'),
    ]

    operations = [
        migrations.DeleteModel(name='TimeDotation'),
        migrations.RunPython(code=copy_data, reverse_code=reverse)
    ]