from jinja2 import Template

manager_template = Template("""from django.db import models
from django.db.models import Q


class {{ classname }}Manager(models.Manager):

    \"""
    Applying a custom QuerySet.
    def get_queryset(self):
        return Custom{{ classname }}QuerySet(self.model, using=self._db)


    In your desired model, assign the manager to one of your model attributes.
    objects = {{ classname }}Manager()
    \"""

    def get_queryset(self):
        return super().get_queryset()
        
    def get_for_user(self, user):
        return self.get_queryset().filter(
            user=user
        )
""")


manager_import_template = Template(
    """from .{{ model.lower() }} import {{ classname }}Manager"""
)
