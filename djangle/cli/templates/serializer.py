from jinja2 import Template


model_serializer = Template(
    """from rest_framework import serializers
{% if model %}from ..models.{{ model.lower() }} import {{ model.capitalize() }}
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
