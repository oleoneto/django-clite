from django import forms
from ..models.{{ name }} import {{ classname }}


class {{ classname }}Form(forms.ModelForm):
    class Meta:
        model = {{ classname }}
        fields = "__all__"
