# {{ if project }}{{ project }}:{% endif %}{{ app }}:routes

"""
Import routes into each view module and append the path to the list:
# {{ project }}/{{ app }}/views.my_view.py
from django.urls import path
from {{ if project }}{{ project }}.{% endif %}{{ app }}.views.routes import routes

def my_view(request):
    ...

routes.append(
    path('', my_view, name='my-view')
)


Append the whole list to your urlpatterns:
# {{ project }}/{{ app }}/urls.py
from {{ if project }}{{ project }}.{% endif %}{{ app }}.views.routes import routes

urlpatterns = [
    ...
] + routes
"""

routes = []
