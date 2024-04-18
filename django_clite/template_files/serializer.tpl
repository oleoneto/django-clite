from rest_framework import serializers
from {{ project }}.{{ app }}.models import {{ classname }}


class {{ classname }}Serializer(serializers.ModelSerializer):
    # Add related fields below:
    # Example relation fields are:
    # -- HyperlinkedIdentityField
    # -- HyperlinkedRelatedField
    # -- PrimaryKeyRelatedField
    # -- SlugRelatedField
    # -- StringRelatedField
    
    # You can also add a custom serializer, like so:
    # likes = LikeSerializer(many=True)

    class Meta:
        model = {{ classname }}
        fields = "__all__"
