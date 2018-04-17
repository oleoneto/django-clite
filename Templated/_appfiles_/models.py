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
