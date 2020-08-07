# {% if project %}{{ project }}:{% endif %}{{ app }}:urls
"""
Import urlpatterns into each view module and append the path to the list:
# {% if project %}{{ project }}/{% endif %}{{ app }}/views.my_view.py
from django.urls import path
from {% if project %}{{ project }}.{% endif %}{{ app }}.views.urls import urlpatterns

def my_view(request):
    # code here...

urlpatterns.append(
    path('', my_view, name='my-view')
)


Append the whole list to your urlpatterns:
# {{ project }}/{{ app }}/urls.py
from {% if project %}{{ project }}.{% endif %}{{ app }}.views.urls import urlpatterns
"""

urlpatterns = []
