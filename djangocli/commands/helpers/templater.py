from jinja2 import Template as JTemplate
import inflect
import re
import pandas

p = inflect.engine()


attribute_template = JTemplate("""{{ name }} = models.{{ type }}({{ options }})""")


model_simple_template = JTemplate("""
class {{ model | capitalize }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
""")

model_template = JTemplate("""
class {{ model | capitalize }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        db_table = '{{ model | capitalize }}_table'
        ordering = ['-created_at']
        {% if abstract %}abstract = True{% endif %}
    
    def __str__(self):
        return self.{% if descriptor %}{{ descriptor }}{% else %}created_at{% endif %}
""")


model_admin_template = JTemplate("""
class {{ model | capitalize }}Admin(admin.ModelAdmin):
    pass
admin.site.register({{ model | capitalize }}, {{model}}Admin)
""")


route_template = JTemplate("""
def {{ route | lower }}(request):
    context = {
        'active': True,
        'route': '{{ route | lower }}',
     }
    return render(request, '{{ route | lower }}.html', context)
""")


route_url_template = JTemplate("""
urlpatterns += [
    path('{% if route == 'index' %}/{% else %}{{ route }}/{% endif %}', {{ route }}, name='{{ route }}'),
]
""")


form_template = JTemplate("""
class {{ model | capitalize }}Form(forms.Form):
    class Meta:
        model = {{ model | capitalize }}
        fields = "__all__"
""")


serializer_template = JTemplate("""
class {{ model | capitalize }}Serializer(serializers.ModelSerializer):
    # If model has foreign key to another model, add it like so:
    # models = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = {{ model | capitalize }}
        fields = "__all__"
""")

viewset_template = JTemplate("""
class {{ model | capitalize }}Viewset(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ model }}.objects.all()
    serializer_class = {{ model | capitalize }}Serializer
""")

html__simple_template = JTemplate("""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ route | capitalize }}</title>
    {% if framework %}<link rel="stylesheet" href="{{ framework }}/css/{{ framework }}.css">
    <script src="{{ framework }}/js/{{ framework }}.js"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route | capitalize }}</h1>
    
    <script src="static/js/main.js"></script>
</body>
</html>
""")

html_template = JTemplate("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ route | capitalize }}</title>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    {% if framework %}<link rel="stylesheet" href="{{ framework[0]['link'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous">
    <script src="{{ framework[1]['src'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route | capitalize }}</h1>
    
    <script src="static/js/main.js"></script>
</body>
</html>
""")

file_serializer_template = JTemplate("""
from rest_framework import serializers
from .models *
""")

file_viewsets_template = JTemplate("""
from rest_framework import viewsets
from .models import *
from .serializers import *
""")

file_app_urls_template = JTemplate("""
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index, name='index'),
]
""")

file_urls_template = JTemplate("""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
import rest_framework.authtoken.views as rf
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
# router.register('model', ModelViewSet)

urlpatterns = [
    # path('/', route, name='route'),
]
""")

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

