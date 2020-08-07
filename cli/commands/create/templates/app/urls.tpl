# {% if project %}{{ project }}:{% endif %}{{ app }}:urls

from django.urls import include, path
from .views.urls import urlpatterns

app_name = "{{ app }}"
