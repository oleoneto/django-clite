from django.urls import path
from django.views.generic import UpdateView
from {{ project }}.{{ app }}.urls import urlpatterns
from {{ project }}.{{ app }}.models import {{ classname }}
from {{ project }}.{{ app }}.forms import {{ classname }}Form


class {{ classname }}UpdateView(UpdateView):
    model = {{ classname }}
    form_class = {{ classname }}Form
    context_object_name = '{{ name }}'
    template_name = '{{ template_name }}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ namespace }}/<slug:slug>/edit', {{ classname }}UpdateView.as_view(), name='{{ name }}-update')
)
