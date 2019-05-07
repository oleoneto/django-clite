import inflect
from jinja2 import Template

IE = inflect.engine()

model_attribute = Template("""{{ name }} = {% if not special %}models.{% endif %}{{ type }}({{ options }})""")


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
from .helpers.identifier import make_identifier
{% for model in imports %}{% if model %}from .{{ model.lower() }} import {{ model.capitalize() }}
{% endif %}{% endfor %}

class {{ model.capitalize() }}(models.Model):
    id = models.BigIntegerField(primary_key=True, editable=False)
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
    # Default fields. Omit with the --no-defaults flag
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = '{{ model.lower() }}'
        ordering = ['-created_at']
        {% if abstract %}abstract = True\n{% endif %}
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = make_identifier()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.{% if descriptor %}{{ descriptor }}{% else %}id{% endif %}
""")


model_test = Template("""from django.test import TestCase
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}TestCase(TestCase):
    def setUp(self):
        # Create objects here...
        # {{ model.capitalize() }}.objects.create()
        # {{ model.capitalize() }}.objects.create()
        pass
        
    def test_{{ model.lower() }}_can_do_something(self):
        # Run assertions here...
        # self.assertEqual()
        pass

""")
