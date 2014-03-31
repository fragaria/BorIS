from operator import methodcaller

from django.core.management import call_command

from south.signals import post_migrate
from south import migration


# Get a list of all the apps that use migrations.
APPS_TO_WAIT_FOR = map(methodcaller('app_label'), migration.all_migrations())


def load_static_data(app, **kwargs):
    global APPS_TO_WAIT_FOR

    APPS_TO_WAIT_FOR.remove(app)

    if len(APPS_TO_WAIT_FOR) == 0:
        print "Loading static fixtures..."
        call_command('loaddata', 'groups')


post_migrate.connect(load_static_data)
