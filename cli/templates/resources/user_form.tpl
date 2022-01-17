from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from ..models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"
