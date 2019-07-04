from jinja2 import Template

router_template = Template("""from rest_framework import routers

'''
Your router endpoints are automatically added to the urlpatterns in urls.py for this app.
To make your app's urls available to the entire project, include your app urls in the urlpatterns for your project:

In your project's urls.py file:

from django.urls import include, path
urlpatterns = [
   # Other paths like admin and login stuff...
   path('{{ app_name }}', include('{{ project_name }}.{{app_name}}.urls'))
]

'''

router = routers.SimpleRouter(trailing_slash=False)
""")
