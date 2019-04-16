from jinja2 import Template

model_admin = Template("""from django.contrib import admin
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


@admin.register({{ model.capitalize() }})
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")

model_import = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}""")


model_admin_inline = Template("""from django.contrib import admin
from ...models.{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}Admin(admin.StackedInline):
    model = {{ model.capitalize() }}
    extra = 1
""")
