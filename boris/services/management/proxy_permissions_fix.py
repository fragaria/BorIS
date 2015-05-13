import sys
from django.apps import apps

from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.db import models

def create_proxy_permissions(app, created_models, verbosity, **kwargs):
    """
        Creates permissions for proxy models which are not created automatically
        by `django.contrib.auth.management.create_permissions`.
        see https://code.djangoproject.com/ticket/11154
        This method is inspired by `django.contrib.auth.managment.create_permissions`.

        Since we can't rely on `get_for_model' we must fallback to `get_by_natural_key`.
        However, this method doesn't automatically create missing `ContentType` so
        we must ensure all the model's `ContentType` are created before running this method.
        We do so by unregistering the `update_contenttypes` `post_syncdb` signal and calling
        it in here just before doing everything.
    """

    try:
        boris_config = apps.get_app_config('boris')
    except:
        raise EnvironmentError('Cannot find app `boris`. App configs are: %s' % apps.get_app_configs())
    update_contenttypes(boris_config, verbosity, **kwargs)
    app_models = models.get_models(app)
    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for model in app_models:
        opts = model._meta
        if opts.proxy:
            # We can't use `get_for_model` here since it doesn't return
            # the correct `ContentType` for proxy models.
            # see https://code.djangoproject.com/ticket/17648
            app_label, model = opts.app_label, opts.object_name.lower()
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            ctypes.add(ctype)
            for perm in _get_all_permissions(opts, model):  # TODO model or contenttype?
                searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're
    # looking for. We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(Permission.objects.filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))
    for ctype, (codename, name) in searched_perms:
        if (ctype.pk, codename) not in all_perms:
            Permission.objects.filter(codename=codename, name=name).delete()
            perm = Permission.objects.create(codename=codename, name=name, content_type=ctype)
            if verbosity >= 2:
                sys.stdout.write("Adding permission '%s'" % perm)


models.signals.post_syncdb.connect(create_proxy_permissions)
# see `create_proxy_permissions` docstring to understand why we unregister
# this signal handler.
models.signals.post_syncdb.disconnect(update_contenttypes)
