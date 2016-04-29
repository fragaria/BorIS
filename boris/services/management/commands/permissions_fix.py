# coding=utf-8
import sys

from django.apps import apps
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand
from django.db import models
from django.db.models.loading import get_app


class Command(NoArgsCommand):
    help = 'test'

    def handle_noargs(self, **options):
        app = get_app('services')
        try:
            boris_config = apps.get_app_config('boris')
        except:
            raise EnvironmentError('Cannot find app `boris`. App configs are: %s' % apps.get_app_configs())
        update_contenttypes(boris_config, 2, interactive=False)
        app_models = models.get_models(app)
        # This will hold the permissions we're looking for as
        # (content_type, (codename, name))
        searched_perms = list()
        # The codenames and ctypes that should exist.
        ctypes = set()
        for model in app_models:
            opts = model._meta
            # We can't use `get_for_model` here since it doesn't return
            # the correct `ContentType` for proxy models.
            # see https://code.djangoproject.com/ticket/17648
            app_label, model = opts.app_label, opts.object_name.lower()
            if app_label == 'services' and model == 'encounter':
                ctype = ContentType.objects.get_by_natural_key(app_label, model)
                ctypes.add(ctype)
                for perm in _get_all_permissions(opts, model):
                    searched_perms.append((ctype, perm))

        # Find all the Permissions that have a content_type for a model we're
        # looking for. We don't need to check for codenames since we already have
        # a list of the ones we're going to create.
        all_perms = set(Permission.objects.filter(
            content_type__in=ctypes,
        ).values_list(
            "content_type", "codename"
        ))

        group, created = Group.objects.get_or_create(name=u'Terén')
        print 'group: %s' % group
        if created:
            print 'ERROR: skupina Teren neexistovala!'
            return
        for ctype, (codename, name) in searched_perms:
            if (ctype.pk, codename) not in all_perms:
                Permission.objects.filter(codename=codename, name=name).delete()
                perm = Permission.objects.create(codename=codename, name=name, content_type=ctype)
                group.permissions.add(perm)
                sys.stdout.write("Adding encounter permission '%s'" % perm)

        for perm in Permission.objects.filter(codename__endswith='_groupcontact'):
            group.permissions.add(perm)
            sys.stdout.write("Adding group encounter permission '%s'" % perm)

        for perm in Permission.objects.filter(codename__endswith='_encounter'):
            group.permissions.add(perm)
            sys.stdout.write("Adding service permission '%s'" % perm)


