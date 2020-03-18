import uuid
from django.db import models
{%- if not api %}
from django.urls import reverse
{%- endif %}
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
{%- if is_managed %}
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
    slug = models.SlugField(_('slug'), max_length=250, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

    {%- if soft_delete %}
    deleted = models.BooleanField(verbose_name=_('deleted'), default=False, editable=False)
    deleted_at = models.DateTimeField(verbose_name=_('deleted at'), auto_now=True, editable=False)
    deleted_by = models.ForeignKey(
            get_user_model(), related_name="deleted_{{ model_plural }}",
            on_delete=models.PROTECT, editable=False,
            verbose_name=_('deleted by'),
            null=True
    )
    {% endif %}

    {%- if is_managed %}
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
        {%- if abstract %}
        abstract = True{%- endif %}
        db_table = '{{ db_table.lower() }}'
        indexes = [models.Index(fields=['created_at'])]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Generate a Medium-like URL slugs:
        # slugify(f'{__SomeCharField__}{str(self.uuid)[-12:]}')
        self.slug = slugify(f'{str(self.uuid)[-12:]}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'
    {% if not api %}
    def get_absolute_url(self):
        return reverse('{{ model.lower() }}-detail', kwargs={'slug': self.slug})
    {%- else -%}{%- endif %}