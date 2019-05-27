from jinja2 import Template

pipfileTemplate = Template("""
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
django-environ = "*"
tox = "*"
textblob = "*"
gunicorn = "*"
psycopg2-binary = "*"
djongo = "*"
django-ckeditor = "*"
django-registration = "*"
django-otp = "*"
django-two-factor-auth = "*"
twilio = "*"
qrcode = "*"
coreapi = "*"
django-rest-swagger = "*"
djangorestframework = ">=3.9.1"
djangorestframework-httpsignature = "*"
djangorestframework-jsonapi = ">=2.6.0"
djangorestframework-simplejwt = "*"
django-filter = ">=2.0.0"
django-oauth-plus = "*"
django-oauth2-provider = "*"
oauth2 = "*"
django-livereload-server = "*"
django-cors-headers = "*"
django-debug-toolbar = "*"
Django = ">=2.2.1"
Pillow = "*"

[requires]
python_version = "3.7"
""")
