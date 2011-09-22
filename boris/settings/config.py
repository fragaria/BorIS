import os
import boris

# helper for building absolute paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(boris.__file__))
p = lambda x: os.path.join(PROJECT_ROOT, x)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'boris.db',
        'USER': '',
        'PASSWORD': '',    },
}

# media serving
MEDIA_ROOT = p('media')
MEDIA_URL = '/media/'

STATIC_ROOT = p('static')
STATIC_URL = '/static/' 

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# cache conf
CACHE_BACKEND = 'dummy://'

# logging conf
LOGGING_CONFIG_FILE = p(os.path.join('settings', 'logger.conf'))

