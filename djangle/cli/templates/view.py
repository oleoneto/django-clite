from jinja2 import Template


function_view_template = Template(
    """from django.shortcuts import HttpResponse
import datetime


def {{ name.lower() }}_view(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>{{ name.capitalize() }}View</h1>It is now %s.</body></html>" % now
    return HttpResponse(html)
""")

view_template = Template("""from django.utils import timezone
from django.views.generic.{{ generic_view_type }} import {{ view_type }}
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ view_name }}({{ view_type }}):
    
    model = {{ model.capitalize() }}
    {% if generic_view_type == 'list' %}paginate_by = 20\n{% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
""")


view_import_template = Template(
    """from .{{ view_file.lower() }} import {{ view_name }}"""
)
