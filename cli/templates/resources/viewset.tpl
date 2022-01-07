from rest_framework import viewsets
from rest_framework import permissions
from {{ project }}.{{ app }}.router import router
from {{ project }}.{{ app }}.models import {{ classname }}
from {{ project }}.{{ app }}.serializers import {{ classname }}Serializer


class {{ classname }}ViewSet(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ classname }}.objects.all()
    serializer_class = {{ classname }}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


router.register('{{ namespace }}', {{ classname }}ViewSet)
