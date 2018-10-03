from os.path import dirname, join

from django.db import connection

from boris import reporting


def install_views(*args, **kwargs):
    cursor = connection.cursor()
    sql_file = open(join(dirname(reporting.__file__), 'sql', 'reporting-views.mysql.sql'), 'r')

    try:
        cursor.execute(sql_file.read())
    finally:
        cursor.close()
        sql_file.close()

