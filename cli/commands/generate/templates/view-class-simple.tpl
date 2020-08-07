from django.views.generic import {{ view_import_name }}
from django.urls import path
from .urls import urlpatterns


class {{ view_name }}({{ view_import_name }}):
    template_name = '{{ template_name }}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ route_name }}', {{ view_name }}.as_view(), name='{{ pattern_name }}')
)
