from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.StringRelatedField(many=True)
    reviews = serializers.StringRelatedField(many=True)

    class Meta:
        model = Artist
        fields = ('name', 'photo', 'albums', 'reviews')


class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)
    reviews = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ('title', 'artwork', 'tracks', 'reviews')


class TrackSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True)

    class Meta:
        model = Track
        fields = ('order', 'title', 'reviews')
