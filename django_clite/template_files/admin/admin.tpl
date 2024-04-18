from django.contrib import admin
from {{ project }}.{{ app }}.models import {{ classname }}


@admin.register({{ classname }})
class {{ classname }}Admin(admin.ModelAdmin):
    {%- if fields %}
    list_display = [{% for attr_name in fields %}
        '{{ attr_name }}',
    {%- endfor %}
    ]
    {% else %}
    list_display = []
    {% endif %}

    {%- if permissions %}
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