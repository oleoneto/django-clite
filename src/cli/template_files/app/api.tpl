# {% if project %}{{ project }}:{% endif %}{{ app }}:api
from django.urls import include, path
from .router import router

app_name = "{{ app }}"

urlpatterns = [
   path('', include(router.urls)),
]
