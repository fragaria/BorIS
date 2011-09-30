import os
import boris

from .base import STATIC_URL

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

STATIC_ROOT = p('static')

# logging conf
LOGGING_CONFIG_FILE = p(os.path.join('settings', 'logger.conf'))

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

