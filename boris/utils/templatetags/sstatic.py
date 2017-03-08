import os

from django import template
from django.conf import settings

from boris import classification

register = template.Library()


@register.simple_tag
def sstatic(path):
    '''
    Returns absolute URL to static file with versioning.
    '''
    full_path = os.path.join(settings.STATIC_ROOT, path)
    try:
        # Get file modification time.
        mtime = os.path.getmtime(full_path)
        return '%s%s?%s' % (settings.STATIC_URL, path, mtime)
    except OSError:
        # Returns normal url if this file was not found in filesystem.
        return '%s%s' % (settings.STATIC_URL, path)


@register.simple_tag
def get_non_application_drugs():
    return str(classification.NON_APPLICATION_DRUGS)