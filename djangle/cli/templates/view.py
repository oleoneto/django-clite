from jinja2 import Template


function_based_view = Template("""from django.shortcuts import HttpResponse
import datetime


def {{ name.capitalize() }}View(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>{{ name.capitalize() }}View</h1>It is now %s.</body></html>" % now
    return HttpResponse(html)
""")

model_list_view = Template("""from django.utils import timezone
from django.views.generic.list import ListView
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}ListView(ListView):
    
    model = {{ model.capitalize() }}
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
""")

model_detail_view = Template("""from django.utils import timezone
from django.views.generic.detail import DetailView
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}DetailView(DetailView):
    
    model = {{ model.capitalize() }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
""")

model_list_view_path = Template("""from django.urls import path
from ..views import {{ model.capitalize() }}View

urlpatterns = [
    path('', {{ model.capitalize() }}View.as_view(), name='{{ model.lower() }}-list'),
]
""")
