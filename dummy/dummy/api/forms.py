from django import forms
from .models import *


class ArtistForm(forms.Form):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumForm(forms.Form):
    class Meta:
        model = Album
        fields = "__all__"
