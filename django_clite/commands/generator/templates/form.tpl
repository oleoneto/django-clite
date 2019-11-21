from django.forms import forms
from ..models.{{ model.lower() }} import {{ classname }}


class {{ classname }}Form(forms.Form):
    class Meta:
        model = {{ classname }}
        fields = "__all__"
