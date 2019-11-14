from jinja2 import Template

manager_template = Template("""from django.db import models, transaction


class Custom{{ classname }}QuerySet(models.QuerySet):
    # Available on both Manager and QuerySet.
    def public_method(self):
        raise NotImplementedError

    # Available only on QuerySet.
    def _private_method(self):
        raise NotImplementedError


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

    @transaction.atomic
    def create_{{ model.lower() }}(self, **kwargs):
        raise NotImplementedError
""")


manager_import_template = Template(
    """from .{{ model.lower() }} import {{ classname }}Manager"""
)
