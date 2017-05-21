import os

from django.core.exceptions import ImproperlyConfigured
from envparse import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env('DCL_SECRET_KEY')

DEBUG = env.bool('DCL_DEBUG', default=True)

DO_INDEX_REDIRECT = env.bool('DCL_DO_INDEX_REDIRECT', default=not DEBUG)

# update it to your domain if you want
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'dcl_server',
    'dcl_server.ui',
    'dcl_server.accreditations',
    'dcl_server.dcl_audit',

    'djangooidc',  # authorize from OIDC providers
    # 'storages',  # push static to S3, not required for web installation if you use CDN
    'raven.contrib.django.raven_compat',  # error reporting
    'crispy_forms',  # bootstrap-like forms by single template tag
    'constance',  # settings in database and django admin panel
    'constance.backends.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dcl_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dcl_server.wsgi.application'

SESSION_COOKIE_NAME = 'dcl-server'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DCL_DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env('DCL_DB_NAME', default='dcl_server'),
        'HOST': env('DCL_DB_HOST', default='localhost'),
        'PORT': env('DCL_DB_PORT', default=5432),
        'USER': env('DCL_DB_USERNAME', default='dcl_server'),
        'PASSWORD': env('DCL_DB_PASSWORD', default='dcl_server'),
        'ATOMIC_REQUESTS': True,
    }
}


AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Static area
STATICFILES_STORAGE = env(
    'DCL_STATICFILES_STORAGE',
    default='django.contrib.staticfiles.storage.StaticFilesStorage'
    # ManifestStaticFilesStorage
)
STATIC_URL = env('DCL_STATIC_URL', default='/static/')
STATIC_ROOT = env(
    'DCL_STATIC_ROOT',
    # if we put here static_root and then run local collectdstatic
    # with manifest file storage, then hashed filenames will be crated
    # and if we change manifested to django-storages then django-storages
    # will copy anything to s3, and Cloudfront will serve it.
    # So need to change web-side static storage to manifested so they can be used.
    # If you don't care about such things then just use StaticFilesStorage for www
    default=os.path.join(BASE_DIR, "../../var/static_root")
)


# # Django-storages area: needed to copy static files to S3 bucket;
# # doesn't really required on WWW if you use CDN, but required otherwise
# AWS_STORAGE_BUCKET_NAME = env('DCL_AWS_STORAGE_BUCKET_NAME', default=None)
# AWS_QUERYSTRING_AUTH = False
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# # it's safe to set such headers if you use hashed filenames, and not always safe in other cases
# # they are django-storages-specific anyway
# # AWS_HEADERS = {
# #     'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
# #     'Cache-Control': 'max-age=94608000',
# # }

# etc

# sentry allows you to be notified about all exceptions your (and our) app raises
RAVEN_DSN = env("DCL_RAVEN_DSN", default=None)
if RAVEN_DSN:
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }

SITE_ID = int(env("DCL_SITE_ID", default=1))

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Business area

# which hostname will be the last part of the target NAPTR record.
# Example: B-FFFFFFFFFFFFFFFFFFFFFFFFFFFF.{DCL_DNS_HOSTNAME}.
DCL_DNS_HOSTNAME = env("DCL_DNS_HOSTNAME", default='dcl.testpoint.io')
if DCL_DNS_HOSTNAME.endswith('.'):
    DCL_DNS_HOSTNAME = DCL_DNS_HOSTNAME[:-1]

# First part of resulting NAPTR record value; usually default is fine
DCL_RECORD_PREFIX = env("DCL_RECORD_PREFIX", default='10 100 "S" "" ""').strip()

# fine value is 300 for prod and something small for development
DCL_NAPTR_RECORD_TTL = env("DCL_NAPTR_RECORD_TTL", default=300)
try:
    DCL_NAPTR_RECORD_TTL = int(DCL_NAPTR_RECORD_TTL)
except (ValueError, TypeError):
    raise ImproperlyConfigured(
        u"Please pass integer value for DCL_NAPTR_RECORD_TTL (got '{}')".format(
            DCL_NAPTR_RECORD_TTL
        )
    )


from .base_oidc import *  # NOQA
from .base_logging import *  # NOQA
from .base_aws import *  # NOQA
from .base_drf import *  # NOQA
from .base_constance import *  # NOQA
