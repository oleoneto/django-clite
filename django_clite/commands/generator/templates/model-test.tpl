from django.test import TestCase
from ..{{ model.lower() }} import {{ classname }}


class {{ classname }}TestCase(TestCase):
    def setUp(self):
        """
        Create objects here...

        Example:
        {{ classname }}.objects.create()
        """

        pass

    def test_create_{{ model.lower() }}(self):
        """
        Run assertions here...

        Example:
        {{ model.lower() }} = {{ classname }}.objects.create()
        self.assertEqual({{ model.lower() }}.id, 1)
        """

        pass
