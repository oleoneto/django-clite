from django.utils import timezone
from django.views.generic import {{ class_type.capitalize() }}View
from django.urls import path
from .urls import urlpatterns
from ..models import {{ classname }}


class {{ classname }}{{ class_type.capitalize() }}View({{ class_type.capitalize() }}View):
    model = {{ classname }}
    context_object_name = '{{ object_name.lower() }}'
    template_name = '{{ model.lower() }}_{{ class_type.lower() }}.html'

    {%- if class_type == 'list' %}
    paginate_by = 20
    {% else %}
    {% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


urlpatterns.append(
    path('{{ route_name }}', {{ classname }}{{ class_type.capitalize() }}View.as_view(), name='{{ view_name }}')
)
