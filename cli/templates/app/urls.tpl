# {% if project %}{{ project }}:{% endif %}{{ app }}:urls

"""
To make this app's urls available to the entire project,
include the urls in the urlpatterns for your project:

In your project's urls.py file (the one close to wsgi.py or settings.py) do so:

from django.urls import include, path
urlpatterns = [
   # Your other url patterns...
   path('{{ app }}/', include('{% if project %}{{ project }}.{% endif %}{{ app }}.urls', namespace='{{ app }}_urls'))
]
"""

from django.urls import include, path
from .router import api

app_name = "{{ app }}"

urlpatterns = [] \
    + api.urlpatterns