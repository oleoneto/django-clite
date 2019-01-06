import inflect
from jinja2 import Template

IE = inflect.engine()

model_attribute = Template("""{{ name }} = models.{{ type }}({{ options }})""")


model_admin = Template(
    """admin.register({{ model.capitalize() }}
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")


model_form = Template(
    """from django.forms import forms
from {{ app }}.models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}Form(forms.Form):
    class Meta:
        model = {{ model.capitalize() }}
        fields = "__all__"
""")


model_simple = Template(
    """from django.db import models


class {{ model.capitalize() }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
""")


model = Template(
    """from django.db import models
{% for model in imports %}{% if model %}from .{{ model.lower() }} import {{ model.capitalize() }}
{% endif %}{% endfor %}

class {{ model.capitalize() }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
    # Default fields. Omit with the --no-defaults flag
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = '{{ model.lower() }}'
        ordering = ['-created_at']
        {% if abstract %}abstract = True\n{% endif %}
    def __str__(self):
        return self.{% if descriptor %}{{ descriptor }}{% else %}created_at{% endif %}
""")
