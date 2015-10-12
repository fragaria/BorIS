from django.core.management import call_command

from south.signals import post_migrate


def load_static_data(app, **kwargs):
    global APPS_TO_WAIT_FOR

    APPS_TO_WAIT_FOR.remove(app)

    if len(APPS_TO_WAIT_FOR) == 0:
        print "Loading static fixtures..."
        call_command('loaddata', 'groups')


post_migrate.connect(load_static_data)
