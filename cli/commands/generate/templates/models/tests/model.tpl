from django.test import TestCase
from {{ project }}.{{ app }}.{{ module }} import {{ classname }}


class {{ classname }}TestCase(TestCase):
    def setUp(self):
        """
        Create sample objects

        Example:
        {{ classname }}.objects.create()
        """

        pass

    def test_create_record(self):
        """
        Run assertions

        Example:
        record = {{ classname }}.objects.create()
        self.assertEqual(record.id, 1)
        """

        pass
