#!/usr/bin/env python

import os
from os.path import join, pardir, abspath, dirname, split
import sys

from django.core.management import execute_from_command_line


# fix PYTHONPATH and DJANGO_SETTINGS for us
# pythonpath dirs
PYTHONPATH = [
    join(dirname(__file__), pardir),
]

# inject few paths to pythonpath
for p in PYTHONPATH:
    if p not in sys.path:
        sys.path.insert(0, p)

# django settings module
default_settings_module = '%s.%s' % (split(abspath(dirname(__file__)))[1], 'settings')
try:
    # django needs this env variable
    if os.environ['DJANGO_SETTINGS_MODULE'] is None:
        raise KeyError
except KeyError, e:
    os.environ['DJANGO_SETTINGS_MODULE'] = default_settings_module


if __name__ == "__main__":
    execute_from_command_line()

