# {{ project }}:{{ app }}:urls

from django.urls import include, path
from .views.routes import routes

app_name = "{{ app }}"

urlpatterns = [
    # path('', my_view, name='')
] + routes
