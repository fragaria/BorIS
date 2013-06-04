"""
In this package, You can find test environment for Ella taggit unittest project.
As only true unittest and "unittest" (test testing programming unit, but using
database et al) are there, there is not much setup around.
"""
import os


test_runner = None
old_config = None

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_boris.settings'


def setup():
    global test_runner
    global old_config
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner()
    test_runner.setup_test_environment()
    old_config = test_runner.setup_databases()

def teardown():
    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()

