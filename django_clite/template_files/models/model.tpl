import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
{% for attr_name, field in imports.items() -%}
from {{ project }}.{{ app }}.models.{{ field.module_name(attr_name) }} import {{ field.klass_name(attr_name) }}
{% endfor %}

class {{ classname }}(models.Model):
    {% for attr_name, f in fields.items() -%}
    {{attr_name}} = models.{{f.kind}}({{ f.field_options(attr_name, classname) }})
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
        # Generate a Medium/Notion-like URL slugs:
        return slugify(f'{str(self.uuid)[-12:]}')

    def get_absolute_url(self):
        return reverse('{{ name.lower() }}-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.slug}'
