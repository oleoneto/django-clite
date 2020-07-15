# cli:commands:create:presets:installable_apps

INSTALLABLE_APPS = {
    'allauth': {
        'apps': [
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
            'allauth.socialaccount.providers.facebook',
            'allauth.socialaccount.providers.google',
            'allauth.socialaccount.providers.linkedin_oauth2',
            'allauth.socialaccount.providers.twitter',
        ],
        'middleware': [],
    },
    'auditlog': {
        'apps': [
            'auditlog',
        ],
        'middleware': [],
    },
    'celery': {
        'apps': [
            'django_celery_beat',
        ],
        'middleware': [],
    },
    'cors': {
        'apps': [
            'corsheaders',
        ],
        'middleware': [
            'corsheaders.middleware.CorsMiddleware',
        ],
    },
    'django-extensions': {
        'apps': [
            'djanjo_extensions',
        ],
        'middleware': [],
    },
    'django-hosts': {
        'apps': [
            'django_hosts',
        ],
        'middleware': [],
    },
    'redis': {
        'apps': [
            'django_redis',
        ],
        'middleware': [],
    },
    'restframework': {
        'apps': [
            'rest_framework',
            'rest_framework.authtoken',
            'rest_framework_httpsignature',
            'rest_framework_swagger',
        ],
        'middleware': [],
    },
    'storages': {
        'apps': [
            'storages',
        ],
        'middleware': [],
    },
    'polymorphic': {
        'apps': [
            'polymorphic',
        ],
        'middleware': [],
    },
    'debug_toolbar': {
        'apps': [
            'debug_toolbar',
        ],
        'middleware': [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ],
    },
    'django_otp': {
        'apps': [
            'django_otp',
            'django_otp.plugins.otp_static',
            'django_otp.plugins.otp_totp',
        ],
        'middleware': [
            'django_otp.middleware.OTPMiddleware',
        ]
    },
}

DEFAULTS = ['allauth', 'cors', 'redis', 'restframework']

APPS = [app for application in INSTALLABLE_APPS for app in INSTALLABLE_APPS[application]['apps']]

MIDDLEWARE = [middleware for application in INSTALLABLE_APPS for middleware in INSTALLABLE_APPS[application]['middleware']]
