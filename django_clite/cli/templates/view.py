from jinja2 import Template


default_function_view_template = Template(
    """from django.shortcuts import HttpResponse
import datetime


def {{ name.lower() }}_view(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>{{ name.capitalize() }}View</h1>It is now %s.</body></html>" % now
    return HttpResponse(html)
""")

default_class_view_template = Template("""from django.utils import timezone{% if list %}
from django.view.generic.list import ListView
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
