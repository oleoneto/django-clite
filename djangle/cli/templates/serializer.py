from jinja2 import Template


serializer_template = Template(
    """from rest_framework import serializers
{% if model %}from ..models import {{ model.capitalize() }}
{% endif %}

class {{ model.capitalize() }}Serializer(serializers.ModelSerializer):
    
    # Add related fields below:
    # Example relation fields are:
    # -- HyperlinkedIdentityField
    # -- HyperlinkedRelatedField
    # -- PrimaryKeyRelatedField
    # -- SlugRelatedField
    # -- StringRelatedField
    
    # You can also create a custom serializer, like so:
    # likes = LikeSerializer(many=True)

    class Meta:
        model = {{ model.capitalize() }}
        fields = "__all__"
""")

serializer_auth_user_template = Template(
    """from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('date_joined', 'updated_at', 'last_login',
                   'is_superuser', 'is_staff', 'user_permissions', 'password')
""")

serializer_import_template = Template(
    """from .{{ model.lower() }} import {{ model.capitalize() }}Serializer"""
)
