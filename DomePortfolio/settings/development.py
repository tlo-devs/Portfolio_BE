from .production import *  # noqa

DEBUG = True
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = [
    "127.0.0.1"
]

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        'rest_framework.permissions.AllowAny'
    ]
