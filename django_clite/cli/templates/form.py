from jinja2 import Template


model_form_template = Template(
    """from django.forms import forms
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}Form(forms.Form):
    class Meta:
        model = {{ model.capitalize() }}
        fields = "__all__"
""")

model_form_import_template = Template(
    """from .{{ model.lower() }} import {{ model.capitalize() }}Form"""
)
