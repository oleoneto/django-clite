from jinja2 import Template

requirements = Template("""# Requirements for {{ project }}

# Django
django>=2.2.1
django-environ


# Models
django-polymorphic


# Caching
django-redis


# Event Queueing, Web workers
gunicorn

# Databases
psycopg2-binary
djongo

# Cloud
cloudinary
boto3
django-storages


# Image Support
Pillow


# WYSIWYG Editor
django-ckeditor


# Authentication
django-registration
django-otp
django-two-factor-auth
twilio
qrcode


# REST API Support
coreapi
django-rest-swagger
djangorestframework>=3.9.1
djangorestframework-httpsignature
djangorestframework-jsonapi>=2.6.0
djangorestframework_simplejwt
django-filter>=2.0.0
django-guardian
django-oauth-plus
django-oauth2-provider
oauth2


# Server
django-livereload-server
django-cors-headers
django-debug-toolbar
""")
