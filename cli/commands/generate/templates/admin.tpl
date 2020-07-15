from django.contrib import admin
from ..models import {{ classname }}


@admin.register({{ classname }})
class {{ classname }}Admin(admin.ModelAdmin):
    list_display = {% if fields %}{{ fields }}{% else %}[field.name for field in {{classname}}._meta.fields]{% endif %}

    {% if permissions %}
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    """
    # For managed models, update the name of the last editor
    def save_model(self, request, obj, form, change):
        if obj.created_by_id is None:
            obj.created_by_id = request.user.id
        obj.updated_by_id = request.user
        super().save_model(request, obj, form, change)
    """
    {%- endif -%}