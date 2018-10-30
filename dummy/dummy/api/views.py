from rest_framework import viewsets
from .serializers import *
from rest_framework_json_api.parsers import JSONParser
from rest_framework_json_api.renderers import JSONRenderer


class ArtistViewset(viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewset(viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewset(viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
