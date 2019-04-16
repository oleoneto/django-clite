from jinja2 import Template

model_admin = Template("""from django.contrib import admin
from ..models.{{ model.lower() }} import {{ model.capitalize() }}


@admin.register({{ model.capitalize() }})
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")

model_import = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}""")
