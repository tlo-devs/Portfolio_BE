import os
import django
from DomePortfolio.docs.settings import *  # noqa
from datetime import timedelta
from .keys import *  # noqa
from django.conf import global_settings
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = Path(BASE_DIR).name

INSTALLED_APPS = [
    'DomePortfolio.custom',  # manage.py overrides
    'DomePortfolio.application.CustomAdmin',  # default admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'drf_yasg',
    'crispy_forms',
    'mptt',
    'imagekit',
    'adminsortable2',
    'djmoney',

    # User defined apps
    'DomePortfolio.apps.users',
    'DomePortfolio.apps.categories',
    'DomePortfolio.apps.portfolio',
    'DomePortfolio.apps.shop',
    'DomePortfolio.apps.orders',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
]

DEBUG = False
AUTH_USER_MODEL = 'users.User'

CRISPY_TEMPLATE_PACK = "bootstrap4"
CURRENCIES = ('USD', 'EUR')

ALLOWED_HOSTS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DomePortfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(django.__path__[0] + '/forms/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Expiration time in Seconds for the product download link
DOWNLOAD_EXPIRY_TIME = 8 * 60 * 60

"""
FILE_UPLOAD_HANDLERS = [
    "DomePortfolio.lib.uploads.handler.UploadProgressCachedHandler"
                       ] + global_settings.FILE_UPLOAD_HANDLERS
"""

# Listing of GCP bucket names by purpose (image PUBLIC, files PRIVATE)
GCP_BUCKETS = {
    "images": f"{PROJECT_NAME}-image-bucket".lower(),
    "files": f"{PROJECT_NAME}-file-bucket".lower(),
}

GCP_KEYFILE_PATH = Path(BASE_DIR).parent / "keys"

WSGI_APPLICATION = 'DomePortfolio.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
