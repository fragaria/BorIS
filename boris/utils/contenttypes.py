from django.apps import apps
from django.contrib.contenttypes.management import update_contenttypes


def update_all_contenttypes(**kwargs):
    for app_config in apps.get_app_configs():
        update_contenttypes(app_config, **kwargs)
