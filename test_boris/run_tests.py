#!/usr/bin/env python

'''
simple shortcut for running nosetests via python
replacement for *.bat or *.sh wrappers

set mysql default collation to utf - http://airbladesoftware.com/notes/fixing-mysql-illegal-mix-of-collations/
'''

import sys
from os.path import abspath, dirname

import nose


def run_all(argv=None):
    sys.exitfunc = lambda msg = 'Process shutting down...': sys.stderr.write(msg + '\n')

    if len(argv) == 1:
        argv = [
            'nosetests',
            '--with-coverage', '--cover-package=boris', '--cover-erase',
            '--nocapture', '--nologcapture',
            '--verbose',
        ]

    nose.run_exit(
        argv=argv,
        defaultTest=abspath(dirname(__file__)),
    )

if __name__ == '__main__':
    run_all(sys.argv)

