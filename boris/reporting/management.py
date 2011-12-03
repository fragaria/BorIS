'''
Created on 3.12.2011

@author: xaralis
'''
from os.path import dirname, join

from django.db import models, connection

from boris import reporting
from boris.reporting import models as reporting_app

def install_views(app, created_models, verbosity, **kwargs):
    if verbosity >= 1:
        print "Installing reporting views ..."
        cursor = connection.cursor()
        sql_file = open(join(dirname(reporting.__file__), 'sql', 'reporting-views.mysql.sql'), 'r')
        cursor.execute(sql_file.read())
        sql_file.close()
        
models.signals.post_syncdb.connect(install_views, sender=reporting_app)