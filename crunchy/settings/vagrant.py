from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG:

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
