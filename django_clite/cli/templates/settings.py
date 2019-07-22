from jinja2 import Template

settings_template = Template("""
# Django settings for {{ project_name }} project.


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True' and os.environ.get('DATABASE_URL') is None

ALLOWED_HOSTS = [] if os.environ.get('LOCAL_MACHINE') else ['{{ domain }}']

INTERNAL_IPS = '127.0.0.1'


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
    'compressor',
    'django_redis',

    # Extras
    'corsheaders',
    'debug_toolbar',

    {% for app in apps %}
    '{{ project_name }}.{{ app }}',
    {% endfor %}
]

MIDDLEWARE = [
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
    {% for middleware in middlewares %}
    '{{ middleware }}',
    {% endfor %}
]

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            {% for app in apps %}
            os.path.join(BASE_DIR, '{{ project_name }}/{{ app }}/templates'),
            {% endfor %}
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

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Database

if "IN_DOCKER" in os.environ:
    # Stuff for when running in Docker-compose.

    CELERY_BROKER_URL = 'redis://redis:6379/1'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/1'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DOCKER_DB_NAME'),
            'USER': os.environ.get('DOCKER_DB_USER'),
            'PASSWORD': os.environ.get('DOCKER_DB_PASSWORD'),
            'HOST': "db",
            'PORT': 5432,
        }
    }

elif "DATABASE_URL" in os.environ:
    USER, PASSWORD, HOST, PORT, NAME = re.match("^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$", os.environ.get("DATABASE_URL", "")).groups()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': int(PORT),
        }
    }

elif "LOCAL_MACHINE" in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
        }
     }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3'
        }
    }

if 'EMAIL_HOST_PASSWORD' in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.getenv('EMAIL_HOST', None)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
    EMAIL_PORT = 587
    
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SERVER_EMAIL = os.environ.get('SERVER_EMAIL')

EMAIL_RELAY_DOMAIN = os.environ.get('EMAIL_RELAY_DOMAIN')


# Password validation

{% if custom_auth %}
AUTH_USER_MODEL = 'authentication.User'

ACCOUNT_USERNAME_VALIDATORS = '{{ project_name }}.authentication.models.validators.username'
{% endif %}

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
SOCIALACCOUNT_PROVIDERS = {}

LOGIN_REDIRECT_URL = '/accounts/me'

ROLEPERMISSIONS_MODULE = '{{ project_name }}.roles'

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

AWS_STATIC_LOCATION = os.environ.get('AWS_STATIC_LOCATION')

AWS_PUBLIC_MEDIA_LOCATION = os.environ.get('AWS_MEDIA_LOCATION')

AWS_PRIVATE_MEDIA_LOCATION = os.environ.get('AWS_PRIVATE_MEDIA_LOCATION')

AWS_DEFAULT_ACL = 'public-read'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_IS_GZIPPED = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/'

STATIC_ROOT = 'staticfiles/'

MEDIA_ROOT = 'mediafiles/'

MEDIA_URL = '/files/'

COMPRESS_ROOT = ''


# Django REST Framework, JWT, and Swagger
# This implementation is JSON-API compatible

REST_FRAMEWORK = {
    'PAGE_SIZE': 25,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',

    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),

    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),

    'SEARCH_PARAM': 'filter[search]',

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),

    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

JSON_API_FORMAT_FIELD_NAMES = 'dasherize'

JSON_API_FORMAT_TYPES = 'dasherize'

JSON_API_PLURALIZE_TYPES = False

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    "LOGIN_URL": 'rest_framework:login',
    "LOGOUT_URL": 'rest_framework:logout',
    "APIS_SORTER": "alpha",
    "DOC_EXPANSION": "None",
    "USE_SESSION_AUTH": True,

    "SHOW_REQUEST_HEADERS": True,
    "CUSTOM_HEADERS": {
      "Accept": "application/vnd.api+json",
      "Content-type": "application/vnd.api+json"
    },

    "ENCODING": "application/vnd.api+json",

    "JSON_EDITOR": True,
    "OPERATIONS_SORTER": 'method',
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "name": "Token ",
            "in": "header"
        }
    },
}


# Error logging and reporting with Sentry

if 'DATABASE_URL' in os.environ:
    # Advanced error reporting in production.
    # Include settings when DOKKU environment is detected.

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )

""")
