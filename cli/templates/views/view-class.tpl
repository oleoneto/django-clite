from django.views.generic import {{ class_type.capitalize() }}View
from django.urls import path
from .urls import urlpatterns
{% if object_name %}from ..models import {{ classname }}{%- endif %}
{% if form_class %}from ..forms import {{ form_class }}{%- endif %}


class {{ classname }}{{ class_type.capitalize() }}View({{ class_type.capitalize() }}View):
    {%- if object_name %}
    model = {{ classname }}
    context_object_name = '{{ object_name.lower() }}'
    {% endif %}
    {%- if form_class %}
    form_class = {{ classname }}Form
    {% endif %}
    template_name = '{{ template_name }}'

    {%- if pagination %}
    paginate_by = 20
    {% else %}
    {% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ route_name }}', {{ classname }}{{ class_type.capitalize() }}View.as_view(), name='{{ view_name }}')
)
