from jinja2 import Template


app_urls_template = Template("""\"""
urlpatterns for {{ project }}.{{ app_name }}
\"""

from django.urls import include, path
from .viewsets.router import router


urlpatterns = [
   path('', include(router.urls)),
]
""")
