from os.path import join, dirname

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = False

SESSION_COOKIE_DOMAIN = None

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'boris'
DATABASE_USER = 'boris'

MEDIA_ROOT = '/srv/boris/repo/boris/media'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

