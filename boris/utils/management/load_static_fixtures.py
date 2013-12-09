from django.conf import settings
from django.core.management import call_command
from south.signals import post_migrate

__author__ = 'xaralis'


APPS_TO_WAIT_FOR = ['clients', 'services']


def load_static_data(app, **kwargs):
    global APPS_TO_WAIT_FOR

    APPS_TO_WAIT_FOR.remove(app)

    if len(APPS_TO_WAIT_FOR) == 0:
        print "Loading static fixtures (Groups)."
        call_command('loaddata', 'groups.json')


#post_migrate.connect(load_static_data)
