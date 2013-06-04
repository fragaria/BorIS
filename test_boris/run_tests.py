#!/usr/bin/env python

'''
simple shortcut for running nosetests via python
replacement for *.bat or *.sh wrappers
'''

import sys
from os.path import abspath, dirname

import nose


def run_all(argv=None):
    sys.exitfunc = lambda msg = 'Process shutting down...': sys.stderr.write(msg + '\n')

    if argv is None:
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

