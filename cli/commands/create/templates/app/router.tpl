from rest_framework import routers

"""
To make this app's urls available to the entire project,
include the app urls in the urlpatterns for your project:

In your project's urls.py file (the one close to settings.py) do so:

from django.urls import include, path
urlpatterns = [
   # Your other url patterns...
   path('{{ app }}', include('{{ project }}.{{ app }}.urls'))
]

"""

router = routers.SimpleRouter(trailing_slash=False)
