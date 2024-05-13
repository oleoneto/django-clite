# {{ project }}:{{ app }}:api
from django.urls import include, path
from rest_framework import routers


app_name = "{{ app }}"

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
   path('', include(router.urls)),
]
