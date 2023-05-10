import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
{% for module in import_list -%}
{% if module -%}from {{ project }}.{{ app }}.models.{{ module.name.lower() }} import {{ module.name.capitalize() }}{% endif %}
{% endfor %}

class {{ classname }}(models.Model):
    {% for field in fields -%}
    {{ field.template() }}
    {% endfor %}
    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

    class Meta:
        {%- if abstract %}
        abstract = True{%- endif %}
        db_table = '{{ table_name }}'
        indexes = [models.Index(fields=['created_at'])]
        ordering = ['-created_at']

    @property
    def slug(self):
        # Generate a Medium-like URL slugs:
        # slugify(f'{__SomeCharField__}{str(self.uuid)[-12:]}')
        return slugify(f'{str(self.uuid)[-12:]}')

    def get_absolute_url(self):
        return reverse('{{ name.lower() }}-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.slug}'
