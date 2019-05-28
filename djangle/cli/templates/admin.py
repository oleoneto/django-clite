from jinja2 import Template

model_admin = Template("""from django.contrib import admin
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


@admin.register({{ model.capitalize() }})
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")

model_admin_import = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}Admin""")


model_admin_inline = Template("""from django.contrib import admin
from ...models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}Inline(admin.StackedInline):
    model = {{ model.capitalize() }}
    extra = 1
""")

model_inline_import = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}Inline""")
