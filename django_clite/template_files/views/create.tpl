from django.urls import path
from django.views.generic import CreateView
from ..urls import urlpatterns
from ..models import {{ classname }}
from ..forms import {{ classname }}Form


class {{ classname }}CreateView(CreateView):
    model = {{ classname }}
    form_class = {{ classname }}Form
    context_object_name = '{{ name }}'
    template_name = '{{ template_name }}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


urlpatterns.append(
    path('{{ namespace }}/new', {{ classname }}CreateView.as_view(), name='{{ name }}-create')
)
