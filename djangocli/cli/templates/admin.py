from jinja2 import Template

admin_imports = Template("""
from django.contrib import admin
""")


model_admin = Template(
    """from models.{{ model.lower() }} import {{ model.capitalize() }}
admin.register({{ model.capitalize() }}
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")
