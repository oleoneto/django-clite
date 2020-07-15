from django.utils import timezone
from django.views.generic import {{ class_type.capitalize() }}View
from django.urls import path
from .routes import routes
from ..models import {{ classname }}


class {{ classname }}{{ class_type.capitalize() }}View({{ class_type.capitalize() }}View):
    model = {{ classname }}
    template_name = '{{ model.lower() }}_{{ class_type.lower() }}.html'
    {% if class_type == 'list' %}paginate_by = 20{% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('{{ route_name }}', {{ classname }}{{ class_type.capitalize() }}View.as_view(), name='{{ view_name }}')
)
