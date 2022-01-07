from django.test import TestCase
from {{ project }}.{{ app }}.{{ name }} import {{ classname }}


class {{ classname }}TestCase(TestCase):
    def setUp(self):
        """
        Create sample objects

        Example:
        {{ classname }}.objects.create()
        """

        pass

    def test_create_{{ name }}(self):
        """
        Run assertions

        Example:
        {{ name }} = {{ classname }}.objects.create()
        self.assertEqual({{ name }}.id, 1)
        """

        pass
