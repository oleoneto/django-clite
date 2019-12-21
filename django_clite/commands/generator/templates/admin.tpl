from django.contrib import admin
from ..models import {{ classname }}


@admin.register({{ classname }})
class {{ classname }}Admin(admin.ModelAdmin):
    {% if not permissions and not fields -%}
    pass
    {% endif -%}

    {% if fields -%}
    list_display = {{ fields }}
    {% endif -%}

    {% if permissions %}
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_superuser

    # Update the name of the last editor
    def save_model(self, request, obj, form, change):
            obj.edited_by_id = request.user
        obj.save
    {% endif %}
