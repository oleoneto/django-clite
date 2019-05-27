file_settings_installed_apps = JTemplate("""
INSTALLED_APPS += [
    # API
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_httpsignature',

    # Cross-Origin Resource Sharing (CORS)
    'corsheaders',

    # Livereload
    'livereload',

]""")

file_settings_middleware = JTemplate("""
MIDDLEWARE += [
    # Cross-Origin Resource Sharing (CORS)
    'corsheaders.middleware.CorsMiddleware',

    # Livereload
    'livereload.middleware.LiveReloadScript',
]""")

file_settings_template_dirs = JTemplate("""'DIRS': [os.path.join(BASE_DIR, 'templates')],""")

file_settings_restframework = JTemplate("""
# REST Framework using Django's standard `django.contrib.auth` permissions,
# or allow read-only access for unauthenticated users.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dummy.auth.APISignatureAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True
""")

file_settings_cors = JTemplate("""
# Cross Origin Resource Sharing 
CORS_ORIGIN_ALLOW_ALL = True""")

regex_for_template_dirs = re.compile(r'\'DIRS\': \[\]')
regex_replacer = """'DIRS': [os.path.join(BASE_DIR, 'templates')],"""

file_settings_local = JTemplate("from settings_local import *")
