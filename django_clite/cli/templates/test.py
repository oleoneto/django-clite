from jinja2 import Template


test_model_template = Template(
    """from django.test import TestCase
from ..models import {{ model.capitalize() }}


class {{ model.capitalize() }}TestCase(TestCase):
    def setUp(self):
        \"""
        Create objects here...

        Example: 
        {{ model.capitalize() }}.objects.create()
        \"""

        pass

    def test_create_{{ model.lower() }}(self):
        \"""
        Run assertions here...

        Example:
        {{ model.lower() }} = {{ model.capitalize() }}.objects.create()
        self.assertEqual({{ model.lower() }}.id, 1)
        \"""

        pass

""")

test_serializer_template = Template(
    """from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from ..{{ model.lower() }} import {{ model.capitalize() }}


class {{ model.capitalize() }}TestCase(APITestCase):

    # The client used to connect to the API
    client = APIClient()

    def setUp(self):
        \"""
        Prepare database and client.
        \"""
        pass

    def test_create_{{ model.lower() }}(self):
        pass

""")

test_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}TestCase""")
