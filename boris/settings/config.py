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
        'PASSWORD': '',
    },
}

STATIC_ROOT = p('static')

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
# List of callables that know how to import templates from various sources.

SECRET_KEY = 'od94mflb73jdjhw63hr7v9jfu7f6fhdujckwlqld87ff'