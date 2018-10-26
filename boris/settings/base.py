# -*- coding: utf-8 -*-
import os
import random
from os.path import dirname, join, abspath

from django.utils.functional import curry

import boris


PROJECT_ROOT = abspath(dirname(boris.__file__))

gettext = lambda s: s

# suppressed -- emails sent by sentry instead
ADMINS = [('Admin', os.environ.get('BORIS_ADMIN_EMAIL'))] if 'BORIS_ADMIN_EMAIL' in os.environ else []
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[%s] ' % os.environ.get('BORIS_INSTALLATION')
EMAIL_HOST = os.environ.get('BORIS_EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('BORIS_EMAIL_PORT', 25)

SECRET_KEY = os.environ.get('BORIS_SECRET_KEY', ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]))

DEBUG = os.environ.get('BORIS_DEBUG', '0') == '1'

ALLOWED_HOSTS = os.environ.get('BORIS_ALLOWED_HOSTS', '').split(',') if 'BORIS_ALLOWED_HOSTS' in os.environ else []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Prague'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'cs'
LOCALE_PATHS = (join(PROJECT_ROOT, "locale"),)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Site ID
SITE_ID = 1

# Absolute path to the directory that holds media.
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

ROOT_URLCONF = 'boris.urls'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    # Serve staticfiles
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(PROJECT_ROOT, 'templates'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_ROOT, '..', 'static')

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"


# Compressed static files
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INSTALLED_APPS = [
    'grappelli.dashboard',
    'grappelli',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',

    # Staticfiles served by WhiteNoise
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'form_utils',
    'raven.contrib.django.raven_compat',

    'boris',

    'boris.clients',
    'boris.services',
    'boris.reporting',
    'boris.impact',
    'boris.syringes',
    'boris.users',
    'boris.utils'
]

# logout the user on browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# store session data in cache if possible
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# after 30 minutes of inactivity, user will be logged out
SESSION_COOKIE_AGE = 60 * 30
SESSION_SAVE_EVERY_REQUEST = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

loggers = ['sentry', 'console'] if 'BORIS_SENTRY_DSN' in os.environ else ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': loggers,
            'propagate': True,
        },
        'celery': {
            'level': 'INFO',
            'handlers': loggers,
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}

# GRAPPELLI RELATED ----------------------------------------------------------
GRAPPELLI_ADMIN_TITLE = gettext(u'<span class="logo"></span> - Elektronická databáze pro evidenci výkonů v sociálních službách')
GRAPPELLI_INDEX_DASHBOARD = 'boris.dashboard.CustomIndexDashboard'

# SENTRY ---------------------------------------------------------------------
# Only configure sentry if dsn is provided
if 'BORIS_SENTRY_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ.get('BORIS_SENTRY_DSN'),
        'name': os.environ.get('BORIS_SENTRY_DSN'),
        'release': boris.__versionstr__,
    }


# Database --------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('BORIS_DB_NAME'),
        'USER': os.environ.get('BORIS_DB_USER'),
        'PASSWORD': os.environ.get('BORIS_DB_PASSWORD'),
        'HOST': os.environ.get('BORIS_DB_HOST', 'localhost'),
        'PORT': os.environ.get('BORIS_DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8',
            'init_command': 'SET '
                'default_storage_engine=MyISAM,'
                'character_set_connection=utf8,'
                'collation_connection=utf8_general_ci'
        },
    },
}

UTILITY_WORK_CHOICES = [('fp', 'FIELD_PROGRAMME', u'1) Terénní programy'),
                        ('cc', 'CONTACT_CENTER', u'2) Kontaktní centrum'),
                        ('mf', 'MEDICAL_FACILITY', u'3) Pobytová léčba'),
                        ('ep', 'EXCHANGE_PROGRAMME', u'4) Výměnný program'),
                        ('t', 'TESTS', u'5) Testy'),
                        ('hs', 'HEALTHCARE_SERVICES', u'6) Zdravotní služby'),
                        ('ss', 'SOCIAL_SERVICES', u'7) Sociální služby'),
                        ('can', 'CANCEL',
                         u'8) Dohoduntý kontakt neproběhl / event. péče ukončena klientem bez dohody'),
                        ('sub', 'SUBSTITUTION', u'9) Substituce'),
                        ('amb', 'AMBULANT_TREATMENT', u'10) Ambulantní léčba'),
                        ('o', 'OTHER', u'11) jiné')]
