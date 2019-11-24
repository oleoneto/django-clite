from django.contrib import admin
from ...models import {{ classname }}


class {{ classname }}Inline(admin.StackedInline):
    model = {{ model.capitalize() }}
    extra = 1
