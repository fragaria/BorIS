# -*- coding: utf-8 -*-
from os.path import dirname, join, abspath
from django.utils.functional import curry

import boris


PROJECT_ROOT = abspath(dirname(boris.__file__))

gettext = lambda s: s

# suppressed -- emails sent by sentry instead
ADMINS = (
#    ('Filip Varecha', 'filip.varecha@fragaria.cz'),
#    ('Hynek Urban', 'hynek.urban@fragaria.cz'),
)
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[BORIS] '

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
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
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

FIXTURE_DIRS = (
   join(PROJECT_ROOT, 'fixtures'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATICFILES_DIRS = (
   join(PROJECT_ROOT, 'static_ex'),
)

STATIC_URL = '/static/'

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
    'django.contrib.staticfiles',

#    'south',  # TODO delete
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

# always freeze south migrations
SOUTH_AUTO_FREEZE_APP = True

# don't run south tests
SKIP_SOUTH_TESTS = True

# logout the user on browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# store session data in cache if possible
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# after 30 minutes of inactivity, user will be logged out
SESSION_COOKIE_AGE = 60 * 30
SESSION_SAVE_EVERY_REQUEST = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# GRAPPELLI RELATED ----------------------------------------------------------
GRAPPELLI_ADMIN_TITLE = gettext(u'<span class="logo"></span> - Elektronická databáze pro evidenci výkonů v sociálních službách')
GRAPPELLI_INDEX_DASHBOARD = 'boris.dashboard.CustomIndexDashboard'

# SENTRY ---------------------------------------------------------------------
RAVEN_CONFIG = {
    'dsn': None,  # set DSN here
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
