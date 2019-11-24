from rest_framework import viewsets
from rest_framework import permissions
from .router import router
from ..models import {{ classname }}
from ..serializers import {{ classname }}Serializer


class {{ classname }}ViewSet(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ classname }}.objects.all()
    serializer_class = {{ classname }}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


router.register('{{ route.lower() }}', {{ classname }}ViewSet)
