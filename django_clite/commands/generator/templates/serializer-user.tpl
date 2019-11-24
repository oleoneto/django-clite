from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'date_joined',
            'updated_at',
            'last_login',
            'is_superuser',
            'is_staff',
            'user_permissions',
            'password'
       )
