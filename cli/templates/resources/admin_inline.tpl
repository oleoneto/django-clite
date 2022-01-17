from django.contrib import admin
from {{ project }}.{{ app }}.admin.models import {{ classname }}


class {{ classname }}Inline(admin.StackedInline):
    model = {{ classname }}
    extra = 0
