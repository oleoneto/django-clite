from django.urls import path
from django.views.generic import ListView
from {{ project }}.{{ app }}.urls import urlpatterns
from {{ project }}.{{ app }}.models import {{ classname }}


class {{ classname }}ListView(ListView):
    model = {{ classname }}
    context_object_name = '{{ namespace }}'
    template_name = '{{ template_name }}'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ namespace }}', {{ classname }}ListView.as_view(), name='{{ name }}-list')
)
