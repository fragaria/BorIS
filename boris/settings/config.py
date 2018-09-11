import os
import boris

from .base import STATIC_URL

# helper for building absolute paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(boris.__file__))
p = lambda x: os.path.join(PROJECT_ROOT, x)

STATIC_ROOT = p('static')

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
