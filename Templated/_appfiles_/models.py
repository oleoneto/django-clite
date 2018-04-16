from _libraries_models import *


class ModelName(models.Model):

    # This is an abstract class. Thus, it cannot be instantiated.

    name = models.CharField(max_length=50, blank=False)
    slug = models.CharField(max_length=50, blank=False)
    #occupation = models.CharField(max_length=50, blank=False)
    #bio = models.TextField(max_length=144, blank=False)
    #photo = models.ImageField(upload_to=uploads/profiles/, max_length=50, blank=False)
    #photo = CloudinaryField('image')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name
