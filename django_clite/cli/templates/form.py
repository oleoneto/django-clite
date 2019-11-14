from jinja2 import Template


model_form_template = Template(
    """from django.forms import forms
from ..models.{{ model.lower() }} import {{ classname }}


class {{ classname }}Form(forms.Form):
    class Meta:
        model = {{ classname }}
        fields = "__all__"
""")

model_form_import_template = Template(
    """from .{{ model.lower() }} import {{ classname }}Form"""
)
