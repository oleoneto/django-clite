# Django-Autogenerator

from _libraries_models import *


class ModelName(models.Model):

    # This is an abstract class. Thus, it cannot be instantiated.
    name = models.CharField(max_length=50, blank=False)
    slug = models.CharField(max_length=50, blank=False)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Audio(models.Model):

    # An audio object related to the portfolio project.
    source = models.FileField(upload_to='uploads/audios/', max_length=60)
    number = models.IntegerField(blank=True)
    title = models.CharField(max_length=50, blank=False)
    artist = models.CharField(max_length=50, blank=False)
    composer = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=15, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        ordering = ['artist']

    def __str__(self):
        return self.title
