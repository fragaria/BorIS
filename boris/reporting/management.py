from os.path import dirname, join

from django.db import connection
from south.signals import post_migrate

from boris import reporting
from boris.reporting import models as reporting_app

def install_views(app, **kwargs):
    print "Installing reporting views ..."
    cursor = connection.cursor()
    sql_file = open(join(dirname(reporting.__file__), 'sql', 'reporting-views.mysql.sql'), 'r')
    try:
        cursor.execute(sql_file.read())
    finally:
        sql_file.close()

post_migrate.connect(install_views, sender=reporting_app)
