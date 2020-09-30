from .production import *  # noqa

DEBUG = True

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        'rest_framework.permissions.AllowAny'
    ]

MIDDLEWARE = [
    # Activate Prometheus metrics
    'django_prometheus.middleware.PrometheusBeforeMiddleware',

    # Activate CORS
    'corsheaders.middleware.CorsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # Let all CSRF checks pass that pass CORS
    'corsheaders.middleware.CorsPostCsrfMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Activate Prometheus metrics
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_REPLACE_HTTPS_REFERER = True

INSTALLED_APPS += ["debug_toolbar"]
INSTALLED_APPS += ["django_prometheus"]
MIDDLEWARE += []
ALLOWED_HOSTS = [
    "*"
]
INTERNAL_IPS = [
    "127.0.0.1"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
