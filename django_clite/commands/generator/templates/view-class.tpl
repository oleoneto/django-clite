from django.utils import timezone{% if class_type == 'list' %}
from django.views.generic.list import ListView
from ..models import {{ classname }}


class {{ classname }}ListView(ListView):
{% else %}
from django.views.generic.detail import DetailView
from ..models import {{ classname }}


class {{ classname }}DetailView(DetailView):
{% endif %}
    model = {{ classname }}
    {% if list %}paginate_by = 20\n{% endif %}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
