from jinja2 import Template


model_viewset = Template(
    """from rest_framework import viewsets
from rest_framework import permissions
from ..models.{{ model.lower() }} import {{ model.capitalize() }}
from ..serializers.{{ model.lower() }} import {{ model.capitalize() }}Serializer


class {{ model.capitalize() }}ViewSet(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ model.capitalize() }}.objects.all()
    serializer_class = {{ model.capitalize() }}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
""")
