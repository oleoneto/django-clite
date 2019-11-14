from jinja2 import Template


default_function_view_template = Template(
    """from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import datetime

\"""
Enable caching if needed.
This page will be cached for 15 minutes.
@cache_page(60 * 15)
\"""
def {{ name.lower() }}_view(request):
    template = "{{ name.lower() }}.html"
    current_date = datetime.datetime.now()
    context = {
        'date': now
    }

    \"""
    Alternatively, your view can return HTML directly like so:
    html = "<html><body><h1>{{ name.capitalize() }}View</h1>It is now %s.</body></html>" % current_date
    return HttpResponse(html)
    \"""
    return render(request, template, context)
""")

default_class_view_template = Template("""from django.utils import timezone{% if class_type == 'list' %}
from django.views.generic.list import ListView
from ..models import {{ classname }}


class {{ classname }}ListView(ListView):
{% else %}
from django.views.generic.detail import DetailView
from ..models import {{ classname }}


class {{ classname }}DetailView(DetailView):
{% endif %}
    model = {{ classname }}
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
    """from .{{ model.lower() }}_{% if class_type == 'list' %}list{% else %}detail{% endif %} import {{ classname }}{% if class_type == 'list' %}ListView{% else %}DetailView{% endif %}"""
)
