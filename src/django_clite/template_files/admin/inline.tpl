from django.contrib import admin
from ...models import {{ classname }}


class {{ classname }}Inline(admin.StackedInline):
    model = {{ classname }}
    extra = 0
