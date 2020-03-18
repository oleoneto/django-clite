from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ..forms.user import CustomUserCreationForm, CustomUserChangeForm
from ..models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['id', 'username', 'name', 'is_staff']
    prepopulated_fields = {'username': ('first_name', 'last_name',)}
