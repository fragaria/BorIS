from operator import methodcaller
from os.path import dirname, join

from django.db import connection

from south import migration
from south.signals import post_migrate

from boris import reporting


# Get a list of all the apps that use migrations.
APPS_TO_WAIT_FOR = map(methodcaller('app_label'), migration.all_migrations())


def install_views(app, **kwargs):
    global APPS_TO_WAIT_FOR

    APPS_TO_WAIT_FOR.remove(app)

    if len(APPS_TO_WAIT_FOR) == 0:
        print "Installing reporting views ..."

        cursor = connection.cursor()
        sql_file = open(join(dirname(reporting.__file__), 'sql', 'reporting-views.mysql.sql'), 'r')

        try:
            cursor.execute(sql_file.read())
        finally:
            sql_file.close()


post_migrate.connect(install_views)
