from os.path import dirname, join

from django.db import connection
from django.db.models.signals import post_syncdb

import boris.reporting.models
from boris import reporting


def install_views(app, **kwargs):
    print "Installing reporting views ..."

    cursor = connection.cursor()
    sql_file = open(join(dirname(reporting.__file__), 'sql', 'reporting-views.mysql.sql'), 'r')

    try:
        cursor.execute(sql_file.read())
    finally:
        sql_file.close()

post_syncdb.connect(install_views, sender=boris.reporting.models)
