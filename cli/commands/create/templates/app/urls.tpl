# {{ if project }}{{ project }}:{% endif %}{{ app }}:urls

from django.urls import include, path
from .views.routes import routes

app_name = "{{ app }}"

urlpatterns = [
    # path('', func_view, name=''),
    # path('', ClassView.as_view(), name=''),
] + routes
