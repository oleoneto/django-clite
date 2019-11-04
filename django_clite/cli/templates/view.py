from jinja2 import Template


default_function_view_template = Template(
    """from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.view.decorators.cache import cache_page
import datetime

\"""
Enable caching if needed. This page will be cached fro 15 minutes.
@cache_page(60 * 15)
\"""
def {{ name.lower() }}_view(request):
    template = "{{ name.lower() }}.html"
    now = datetime.datetime.now()
    context = {
        'date': now
    }

    \"""
    Alternatively, your view can return HTML directly like so:
    html = "<html><body><h1>{{ name.capitalize() }}View</h1>It is now %s.</body></html>" % now
    return HttpResponse(html)
    \"""
    return render(request, template, context)
""")

default_class_view_template = Template("""from django.utils import timezone{% if list %}
from django.views.generic.list import ListView
from ..models import {{ model.capitalize() }}


class {{ model.capitalize() }}ListView(ListView):
{% else %}
from django.view.generic.detail import DetailView
from ..models import {{ model.capitalize() }}


class {{ model.capitalize() }}DetailView(DetailView):
{% endif %}
    model = {{ model.capitalize() }}
    {% if list %}paginate_by = 20\n{% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
""")

function_view_import_template = Template(
    """from .{{ model.lower() }} import {{ model.lower() }}"""
)

default_function_view_import_template = Template(
    """from .{{ name.lower() }} import {{ name.lower() }}_view"""
)

default_class_view_import_template = Template(
    """from .{{ model.lower() }} import {{ model.capitalize() }}{% if list %}ListView{% elif detail %}DetailView{% endif %}"""
)
