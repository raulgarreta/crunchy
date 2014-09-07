from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG:

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)

    # Additional locations of static files
    STATICFILES_DIRS.append(abspath(join(ROOT_DIR, 'frontend')))

