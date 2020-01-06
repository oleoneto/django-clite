import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
{%- if is_user_managed %}
from django.contrib.auth import get_user_model
{%- endif %}
{% for model in imports -%}
{% if model -%}from {{ model[0] }} import {{ model[1] }}{% endif %}
{% endfor -%}
{% if base -%}from {{ base[0] }} import {{ base[1] }}
{% endif %}

class {{ classname }}({% if base %}{{ base[1] }}{% else %}models.Model{% endif %}):
    {% for field in fields -%}
    {{ field }}
    {% endfor %}
    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

    {%- if is_user_managed %}
    created_by = models.ForeignKey(
            get_user_model(), related_name="created_{{ model_plural }}",
            on_delete=models.PROTECT, editable=False,
            verbose_name=_('created by'),
            null=True
    )
    updated_by = models.ForeignKey(
            get_user_model(), related_name="updated_{{ model_plural }}",
            on_delete=models.PROTECT, editable=False,
            verbose_name=_('updated by'),
            null=True
    )
    {%- endif %}

    class Meta:
        {% if abstract %}
        abstract = True
        {%- endif %}
        db_table = '{{ db_table.lower() }}'
        indexes = [models.Index(fields=['created_at'])]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'

    def get_absolute_url(self):
        return reverse('{{ model.lower() }}-detail', kwargs={'pk': self.pk})
