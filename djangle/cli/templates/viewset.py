from jinja2 import Template
from inflect import engine

pl = engine()


model_viewset = Template(
    """from rest_framework import viewsets
from rest_framework import permissions
from .router import router
from ..models.{{ model.lower() }} import {{ model.capitalize() }}
from ..serializers.{{ model.lower() }} import {{ model.capitalize() }}Serializer


class {{ model.capitalize() }}ViewSet(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ model.capitalize() }}.objects.all()
    serializer_class = {{ model.capitalize() }}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


router.register('{{ route.lower() }}', {{ model.capitalize() }}ViewSet)
""")

ViewSetImportTemplate = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}ViewSet""")
