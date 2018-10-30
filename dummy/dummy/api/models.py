from django.db import models


class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='artists', blank=True)

    class Meta:
        db_table = 'dummy_artists'
        ordering = ['first_name']

    def name(self):
        if self.last_name:
            _name = "{} {}".format(self.first_name, self.last_name)
        else:
            _name = self.first_name
        return _name

    def __str__(self):
        return self.name()


class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    artwork = models.ImageField(upload_to='albums', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'dummy_albums'
        ordering = ['artist', 'title']

    def info(self):
        return "{}\n{}".format(self.title, self.artist.name())

    def __str__(self):
        return self.title


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'dummy_tracks'
        unique_together = ('album', 'order')
        ordering = ['order', 'title']

    def __str__(self):
        return "{} {}".format(self.order, self.title)


# ---------------------------


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.title


class ArtistReview(Review):
    artist = models.ForeignKey(Artist, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dummy_artist_reviews'


class AlbumReview(Review):
    album = models.ForeignKey(Album, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dummy_album_reviews'


class TrackReview(Review):
    track = models.ForeignKey(Track, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dummy_track_reviews'
