[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
# Django Framework
django = ">=2.2.1"

# API Support
coreapi = "*"
djangorestframework = ">=3.9.1"
djangorestframework-jsonapi = ">=2.6.0"
django-filter = ">=2.0.0"
django-rest-swagger = "*"
drf-dynamic-fields = "*"
drf-flex-fields = "*"
drf-nested-routers = "*"

# Authentication and Permissions
djangorestframework-httpsignature = "*"
djangorestframework-simplejwt = "*"
django-cors-headers = "*"
django-allauth = "*"
django-guardian = "*"
django-hijack = "*"
django-oauth-plus = "*"
django-oauth2-provider = "*"
django-otp = "*"
django-registration = "*"
django-role-permissions = "*"
django-two-factor-auth = "*"
oauth2 = "*"
qrcode = "*"
twilio = "*"
django-letsencrypt = "*"

# Caching and Storage
boto3 = "*"
cloudinary = "*"
django-compress = "*"
django-compressor = "*"
django-redis = "*"
django-storages = "*"
Pillow = "*"

# Debugging and Testing
coverage = "*"
django-debug-toolbar = "*"
django-extensions = "*"
django-livereload-server = "*"
health-check = "*"
jupyterlab = "*"
python-coveralls = "*"
sentry-sdk = "*"

# Database and Custom Type Support
django_polymorphic = "*"
django-recurrence = "*"
django-tenant-schemas = "*"
djongo = "*"
psycopg2-binary = "*"

# Environments
django-environ = "*"
python-dotenv = "*"

# Miscellaneous
django-widget-tweaks = "*"

# Payments
stripe = "*"

# Servers, Web-workers, and Sockets
channels = "*"
gunicorn = "*"
werkzeug = "*"

# Text Editors
django-ckeditor = "*"


[requires]
python_version = "3.7"
