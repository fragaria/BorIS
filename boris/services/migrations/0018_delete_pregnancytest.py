# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations


def reconvert_tests(apps, schema_editor):
    pass


def convert_tests(apps, schema_editor):
    # convert PregnancyTest to UrineTest.pregnancy_test
    PregnancyTest = apps.get_model('services', 'PregnancyTest')
    UrineTest = apps.get_model('services', 'UrineTest')

    ct = ContentType.objects.get_by_natural_key('services', 'pregnancytest')
    for ic in PregnancyTest.objects.filter(content_type_id=ct.id):
        new = UrineTest(encounter=ic.encounter, title=UrineTest._meta.verbose_name)
        new.created = ic.created
        new.modified = ic.modified
        new.pregnancy_test = True
        ct = ContentType.objects.get_for_model(new)
        new.content_type_id = ct.id
        new.save()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_delete_individualcounseling'),
    ]

    operations = [
        migrations.RunPython(convert_tests, reverse_code=reconvert_tests),
        migrations.DeleteModel(
            name='PregnancyTest',
        ),
    ]
