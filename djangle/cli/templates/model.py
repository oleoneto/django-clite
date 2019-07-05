import inflect
from jinja2 import Template

IE = inflect.engine()

model_field_template = Template("""{{ name }} = {% if not special %}models.{% endif %}{{ type }}({{ options }})""")


model_admin_template = Template("""admin.register({{ model.capitalize() }}
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")


model_form_template = Template("""from django.forms import forms
from {{ app }}.models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}Form(forms.Form):
    class Meta:
        model = {{ model.capitalize() }}
        fields = "__all__"
""")


model_template = Template("""import uuid
from django.db import models
{% for model in imports %}{% if model %}from .{{ model.lower() }} import {{ model.capitalize() }}
{% endif %}{% endfor %}

class {{ model.capitalize() }}(models.Model):
    {% for field in fields %}{{ field }}
    {% endfor %}
    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = '{{ db_table.lower() }}'
        ordering = ['-created_at']
        {% if abstract %}abstract = True\n{% endif %}
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'
""")

model_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}""")
