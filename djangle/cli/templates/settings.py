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

ALLOWED_HOSTS = [] if os.environ.get.get('LOCAL_MACHINE') else ['{{ domain }}']

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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

if "IN_DOCKER" in os.environ.get:
    # Stuff for when running in Docker-compose.

    CELERY_BROKER_URL = 'redis://redis:6379/1'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/1'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "postgres",
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': "db",
            'PORT': 5432,
        }
    }

elif "DATABASE_URL" in os.environ.get:
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

elif "LOCAL_MACHINE" in os.environ.get:
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
            'NAME': 'dev.sqlite3'
        }
    }

if os.environ.get('EMAIL_HOST_PASSWORD'):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)
    EMAIL_PORT = 587
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SERVER_EMAIL = os.environ.get('SERVER_EMAIL')


# Password validation

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
""")
