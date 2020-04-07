# {{ project }}:{{ app }}:urls

from django.urls import include, path
from .views.routes import routes


urlpatterns = [
    # path('', my_view, name='')
] + routes
