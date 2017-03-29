# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations

from boris.clients.models import Anonymous


def update_thc_users(apps, schema_editor):
    AnonymousMig = apps.get_model('clients', 'Anonymous')
    ct = ContentType.objects.get_for_model(AnonymousMig)

    woman = Anonymous.objects.get(sex=1, drug_user_type=5, content_type=ct)
    woman.title = 'žena - uživatelka THC'
    woman.save()
    man = Anonymous.objects.get(sex=2, drug_user_type=5, content_type=ct)
    man.title = 'muž - uživatel THC'
    man.save()
    print "Successfully updated anonymous users"


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_auto_20170125_1224'),
    ]

    operations = [
        migrations.RunPython(update_thc_users)
    ]
