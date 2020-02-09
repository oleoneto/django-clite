"""
Django settings for {{ project }} project.
"""

import os
import re
from dotenv import load_dotenv

# Read values from system environment
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG'))

ALLOWED_HOSTS = {% if domain %}['{{ domain }}']{% else %}[]{% endif %}

INTERNAL_IPS = '127.0.0.1'


# Stripe account information. Use TEST values in DEBUG mode.

STRIPE_LIVE_MODE = False if DEBUG else bool(os.environ.get('STRIPE_LIVE_MODE'))

STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')

STRIPE_TEST_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY')

STRIPE_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY') \
    if DEBUG else os.environ.get('STRIPE_LIVE_SECRET_KEY')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY') \
    if DEBUG else os.environ.get('STRIPE_LIVE_PUBLISHABLE_KEY')


# Application definition

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',

    # Authentication and Authorisation
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.twitter',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',

    'rolepermissions',
    'guardian',

    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_httpsignature',
    'rest_framework_swagger',
    
    # File storage and caching
    'storages',
    'django_redis',

    # Extras
    'corsheaders',
    'ckeditor',
    'debug_toolbar',

    {% if apps %}# {{ project }} apps{% for app in apps %}
    '{{ project }}.{{ app }}.apps.{{ app.capitalize() }}Config',{% endfor %}{% endif %}
]

MIDDLEWARE = [
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware', # <-- Caching
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', # <-- Caching
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = '{{ project }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [{% if apps %}{% for app in apps %}
            os.path.join(BASE_DIR, '{{ project }}/{{ app }}/templates'),{% endfor %}{% endif %}
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

WSGI_APPLICATION = '{{ project }}.wsgi.application'


# Database

ENGINE = 'django.db.backends.postgresql'

if "DATABASE_URL" in os.environ:

    USER, PASSWORD, HOST, PORT, NAME = re.match("^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$", os.environ.get("DATABASE_URL", "")).groups()

    DATABASES = {
        'default': {
            'ENGINE': ENGINE,
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': int(PORT),
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': ENGINE,
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
     }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "{{ project }}"
    }
}

CACHE_TTL = 60 * 15

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "") + "/1"

CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "") + "/1"

CELERY_TASK_ALWAYS_EAGER = True

# CELERY_ACCEPT_CONTENT = ['application/json']

# CELERY_TASK_SERIALIZER = 'json'

# CELERY_RESULT_SERIALIZER = 'json'

# Email server backend configuration
# Use SendGrid to deliver automated email

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Password validation

AUTH_USER_MODEL = 'authentication.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

# https://django-allauth.readthedocs.io/en/latest/providers.html

# ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_USERNAME_MIN_LENGTH = 6

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = int(os.environ.get('ACCOUNT_LOGIN_ATTEMPTS_LIMIT'))

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = int(os.environ.get('ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT'))

ACCOUNT_USERNAME_BLACKLIST = os.environ.get('ACCOUNT_USERNAME_BLACKLIST')

ACCOUNT_LOGOUT_REDIRECT_URL = '/'

LOGIN_REDIRECT_URL = '/accounts/me/'

SOCIALACCOUNT_QUERY_EMAIL = True

GUARDIAN_RAISE_403 = True

OTP_TOTP_ISSUER = os.environ.get('OTP_ISSUER')


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

AWS_S3_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_CUSTOM_DOMAIN')

AWS_LOCATION = os.environ.get('AWS_LOCATION')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_IS_GZIPPED = True

DEFAULT_FILE_STORAGE = '{{ project }}.storage.PublicFileStorage'

STATICFILES_STORAGE = '{{ project }}.storage.StaticStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/'

STATIC_ROOT = 'staticfiles/'

MEDIA_ROOT = 'mediafiles/'

MEDIA_URL = '/files/'


# Django REST Framework, JWT, and Swagger configurations go here.

# REST_FRAMEWORK = {}

# SIMPLE_JWT = {}

# SWAGGER_SETTINGS = {}


# Error logging and reporting with Sentry
# Advanced error reporting in production.

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
        RedisIntegration()
    ]
)
