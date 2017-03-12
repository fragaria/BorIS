# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations
from django.db.models import Q


def reconvert_social_work(apps, schema_editor):
    pass


def convert_social_work(apps, schema_editor):
    """
    Migrations 0014 - 0017 take care of a major change in services categorization.
    IndividualCounseling is converted to non-proxy IndividualCounselling, with default 'other' sub-service.
    Moreover SocialWork sub-services are converted and removed:
    - SocialWork.counselling to IndividualCounselling.pre_treatment
    - SocialWork.work_with_family to WorkWithFamily

    1 Create non-proxy IndividualCounselling
    2 Convert old SocialWork and IndividualCounseling sub-services
    3 Add new/remove old SocialWork fields
    4 Remove old IndividualCounseling
    """
    # convert IndividialCounseling to IndividualCounselling.general
    # convert old SocialWork.counselling to IndividualCounselling.pre_treatment
    # convert old SocialWork.work_with_family to WorkWithFamily
    SocialWork = apps.get_model('services', 'SocialWork')
    WorkWithFamily = apps.get_model('services', 'WorkWithFamily')
    IndividualCounseling = apps.get_model('services', 'IndividualCounseling')
    IndividualCounselling = apps.get_model('services', 'IndividualCounselling')

    try:
        ct = ContentType.objects.get_by_natural_key('services', 'individualcounseling')
        for ic in IndividualCounseling.objects.filter(content_type_id=ct.id):
            _convert(IndividualCounselling, ic, {'general': True})
            ic.delete()
    except ContentType.DoesNotExist:
        pass  # new installations don't have the ct

    try:
        ct = ContentType.objects.get_by_natural_key('services', 'socialwork')
        for service in SocialWork.objects.filter(Q(counselling=True) | Q(work_with_family=True), content_type_id=ct.id):
            if service.counselling:
                _convert(IndividualCounselling, service, {'pre_treatment': True})
                print 'Converted counselling to IC.pre_treatment %s' % service.encounter
                service.counselling = False
            if service.work_with_family:
                _convert(WorkWithFamily, service)
                print 'Converted wwf to WorkWithFamily %s' % service.encounter
                service.work_with_family = False
            service.save()
            if not any([getattr(service, attr.attname) for attr in SocialWork._meta.fields
                        if attr.attname not in ('encounter_id', 'id', 'service_ptr_id', 'content_type_id', 'title', 'created', 'modified')]):
                print 'Deleting empty SocialWork %s' % service.encounter
                service.delete()
    except ContentType.DoesNotExist:
        pass  # new installations don't have the ct


def _convert(clazz, s, values=None):
    if values is None:
        values = {}
    new = clazz(encounter=s.encounter, title=clazz._meta.verbose_name)
    new.created = s.created
    new.modified = s.modified
    for k, v in values.iteritems():
        setattr(new, k, v)
    ct = ContentType.objects.get_for_model(new)
    new.content_type_id = ct.id
    new.save()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_individualcounselling'),
    ]

    operations = [
        migrations.RunPython(convert_social_work, reverse_code=reconvert_social_work)
    ]
