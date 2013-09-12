from logging import LOGGING

DEBUG = True

# Don't log to sentry on local.
LOGGING['root']['handlers'] = ['console']
LOGGING['loggers']['django.request'] = {
    'level': 'ERROR',
    'handlers': ['console'],
    'propagate': False,
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
