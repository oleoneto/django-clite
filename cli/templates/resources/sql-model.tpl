import uuid
from django.db import models
{% for model in imports %}{% if model %}from .{{ model[0] }} import {{ model[1] }}{% endif %}
{% endfor %}
{% if base %}from {{ base[0] }} import {{ base[1] }}\n\n{% endif %}
class {{ classname }}({% if base %}{{ base[1] }}{% else %}models.Model{% endif %}):
    {% for field in fields %}{{ field }}
    {% endfor %}
    class Meta:
        db_table = '{{ db_table.lower() }}'
        managed = False
