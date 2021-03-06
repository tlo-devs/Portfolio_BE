import os
from datetime import timedelta
from pathlib import Path

import django
import mimetypes
from DomePortfolio.lib.utils import Tfvars

from DomePortfolio.docs.settings import *  # noqa
from .keys import *  # noqa
from .prod_admin import *  # noqa

mimetypes.add_type("text/css", ".css", True)  # fix issue with CSS files in deployment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = Path(BASE_DIR).name
TERRAFORM = Tfvars(Path(BASE_DIR).parent / ".terraform" / "terraform.tfvars")

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
    'corsheaders',

    # User defined apps
    'DomePortfolio.apps.users',
    'DomePortfolio.apps.categories',
    'DomePortfolio.apps.portfolio',
    'DomePortfolio.apps.shop',
    'DomePortfolio.apps.orders',
    'DomePortfolio.apps.content',
]

# This is assuming CloudSQL Proxy works so we can migrate before App Engine deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': "localhost",
        'PORT': "5432",
        'NAME': "domeportfolio-main-database",
        'USER': TERRAFORM.vars.db_username,
        'PASSWORD': TERRAFORM.vars.db_password,
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
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

# Check if we are in Docker container
if os.getenv("UWSGI_INI", None):
    STATIC_ROOT = '/var/django/projects/DomePortfolio/static/'  # noqa
else:
    STATIC_ROOT = 'static'  # noqa

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
]

DEBUG = False
AUTH_USER_MODEL = 'users.User'

CRISPY_TEMPLATE_PACK = "bootstrap4"
CURRENCIES = ('USD', 'EUR')

ALLOWED_HOSTS = [
    ".11sevendome.de",
    ".tlo-devs.com",
    ".appspot.com",
]

# CORS Configuration
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',
    'HEAD',
]
CORS_EXPOSE_HEADERS = [
    "Content-Disposition"
]
CORS_ALLOWED_ORIGINS = [
    "https://www.11sevendome.de"
]
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

# Listing of GCP bucket names by purpose (image PUBLIC, files PRIVATE)
GCP_BUCKETS = {
    "images": f"{PROJECT_NAME}-image-store".lower(),
    "files": f"{PROJECT_NAME}-file-store".lower(),
    "videos": f"{PROJECT_NAME}-video-store".lower(),
}

GCP_KEYFILE_PATH = Path(BASE_DIR).parent / "keys"
GCP_STORAGE_KEY = GCP_KEYFILE_PATH / "storage_ops.json"
GCP_LOGGING_KEY = GCP_KEYFILE_PATH / "logging_ops.json"

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

if os.getenv("GAE_APPLICATION", None):
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "cloudsql")

    # When using GAE use a unix socket for connection to the db instead
    DATABASES["default"]["HOST"] = f"/{db_socket_dir}/{CLOUD_SQL_CONN_NAME}"

    # Setup Google Cloud Logging
    from google.cloud import logging  # noqa
    client = logging.Client().from_service_account_json(
        GCP_LOGGING_KEY
    )
    # Connects the logger to the root logging handler; by default
    # this captures all logs at INFO level and higher
    client.setup_logging()
    LOGGING = {
        'version': 1,
        'handlers': {
            'stackdriver': {
                'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
                'client': client
            }
        },
        'loggers': {
            '': {
                'handlers': ['stackdriver'],
                'level': 'INFO',
                'name': os.getenv("GAE_DEPLOYMENT_ID", "default")
            }
        },
    }
