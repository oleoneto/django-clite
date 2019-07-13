from jinja2 import Template


viewset_template = Template(
    """from rest_framework import viewsets
from rest_framework import permissions
from .router import router
from ..models import {{ model.capitalize() }}
from ..serializers import {{ model.capitalize() }}Serializer


class {{ model.capitalize() }}ViewSet(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ model.capitalize() }}.objects.all()
    serializer_class = {{ model.capitalize() }}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


router.register('{{ route.lower() }}', {{ model.capitalize() }}ViewSet)
""")

viewset_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}ViewSet""")
