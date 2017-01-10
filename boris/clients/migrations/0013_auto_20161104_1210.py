# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from boris.clients.models import Anonymous


def create_thc_users(apps, schema_editor):
    AnonymousMig = apps.get_model('clients', 'Anonymous')
    ct = ContentType.objects.get_for_model(AnonymousMig)

    man, created_m = Anonymous.objects.get_or_create(
        sex=1, drug_user_type=5, content_type=ct, title='muž - uživatel THC')
    woman, created_w = Anonymous.objects.get_or_create(
        sex=2, drug_user_type=5, content_type=ct, title='žena - uživatelka THC')
    print "Successfully created %s anonymous users" % sum((created_m, created_w))


class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0012_remove_groupcontact_name'),
    ]

    operations = [
        migrations.RunPython(create_thc_users)
    ]
