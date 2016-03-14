from django.contrib.auth.models import Permission
from django.db import models


def delete_proxy_permissions(sender, **kwargs):
    """
        UPDATE: Permissions are still not fixed in Dj1.6 so we remove
        them in order not to confuse the user.

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

    if sender.name == 'boris.services':
        permissions = Permission.objects.filter(content_type__app_label='services')\
            .exclude(codename__endswith='_service')

        print "Deleting %s permissions..." % permissions.count()
        permissions.delete()
        print "Done."


models.signals.post_migrate.connect(delete_proxy_permissions)
