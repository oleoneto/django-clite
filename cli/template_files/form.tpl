from django import forms
from {{ project }}.{{ app }}.models.{{ name }} import {{ classname }}


class {{ classname }}Form(forms.ModelForm):
    class Meta:
        model = {{ classname }}
        fields = "__all__"
