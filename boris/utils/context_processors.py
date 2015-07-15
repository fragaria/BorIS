from django.conf import settings

__author__ = 'ondrej'


def active_modules(request):
    return {
        'ACTIVE_MODULE_CONFIG': settings.ACTIVE_MODULE_CONFIG
    }
