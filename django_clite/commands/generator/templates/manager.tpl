from django.db import models
from django.db.models import Q


class {{ classname }}Manager(models.Manager):

    """
    Applying a custom QuerySet.
    def get_queryset(self):
        return Custom{{ classname }}QuerySet(self.model, using=self._db)


    In your desired model, assign the manager to one of your model attributes.
    objects = {{ classname }}Manager()

    If you want to create fixtures by passing ['field1', 'field2']:
    def get_by_natural_key(self, field1, field2):
        return self.get(field1=field1, field2=field2)
    """

    def get_queryset(self):
        return super().get_queryset().prefetch_related()

    def get_for_user(self, user):
        return self.get_queryset().filter(user=user)
