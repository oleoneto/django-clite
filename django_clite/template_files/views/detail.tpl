from django.urls import path
from django.views.generic import DetailView
from {{ project }}.{{ app }}.urls import urlpatterns
from {{ project }}.{{ app }}.models import {{ classname }}


class {{ classname }}DetailView(DetailView):
    model = {{ classname }}
    context_object_name = '{{ name }}'
    template_name = '{{ template_name }}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ namespace }}/<slug:slug>', {{ classname }}DetailView.as_view(), name='{{ name }}-detail')
)
