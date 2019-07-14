from jinja2 import Template

model_admin_template = Template(
    """from django.contrib import admin
from ..models import {{ model.capitalize() }}


@admin.register({{ model.capitalize() }})
class {{ model.capitalize() }}Admin(admin.ModelAdmin):
    pass
""")


admin_user_auth_template = Template(
    """from django.contrib import admin
from django.contrib.auth.admin import (
    AdminPasswordChangeForm,
    UserAdmin as BaseUserAdmin,
    UserChangeForm,
    UserCreationForm
)
from ..models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['id', 'username', 'name', 'is_staff', 'token']
    prepopulated_fields = {'username': ('first_name', 'last_name',)}
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    readonly_fields = ('date_joined', 'last_login',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'photo'),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
""")


model_admin_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}Admin""")


model_admin_inline_template = Template(
    """from django.contrib import admin
from ...models import {{ model.capitalize() }}


class {{ model.capitalize() }}Inline(admin.StackedInline):
    model = {{ model.capitalize() }}
    extra = 1
""")

model_inline_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}Inline""")
