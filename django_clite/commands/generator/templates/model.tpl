import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
{% for model in imports %}{% if model %}from .{{ model[0] }} import {{ model[1] }}{% endif %}
{% endfor %}
{% if base %}from {{ base[0] }} import {{ base[1] }}\n\n{% endif %}
class {{ classname }}({% if base %}{{ base[1] }}{% else %}models.Model{% endif %}):
    {% for field in fields %}{{ field }}
    {% endfor %}
    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('uploaded at'), auto_now=True, editable=False)

    class Meta:
        db_table = '{{ db_table.lower() }}'
        ordering = ['-created_at']
        {% if abstract %}abstract = True\n{% endif %}
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'
