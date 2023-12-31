from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
# from {{ project }}.{{ app }}.models import MyModel


class Command(BaseCommand):
    help = "What this command does"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Example:

        try:
            [MyModel.objects.create(**i) for i in [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]]
        except IntegrityError:
            print(f'Skipping creation of record {i} it seems to already exist.')
        """

        pass
