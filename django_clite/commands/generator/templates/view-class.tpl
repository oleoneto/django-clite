from django.utils import timezone
from django.views.generic import {{ class_type.capitalize() }}View
{% if class_type == 'form' -%}from .forms import {{ classname }}Form{%- endif %}
from ..models import {{ classname }}


class {{ classname }}{{ class_type.capitalize() }}View({{ class_type.capitalize() }}View):
    model = {{ classname }}
    template_name = '{{ model.lower() }}_{{ class_type.lower() }}.html'
    {% if class_type == 'list' -%}
    paginate_by = 20
    {% elif class_type == 'form' -%}
    form_class = {{ classname }}Form
    # success_url = '/success/'
    {%- endif %}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
