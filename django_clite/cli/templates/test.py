from jinja2 import Template


test_case_template = Template(
    """from django.test import TestCase
from ..models import {{ model.capitalize() }}


class {{ model.capitalize() }}TestCase(TestCase):
    def setUp(self):
        \"""
        Create objects here...
        
        Example: 
        Album.objects.create(title='Djangle Today', is_compilation=True)
        \"""
        
        pass

    def test_{{ model.lower() }}_can_do_something(self):
        \"""
        Run assertions here...
        
        Example:
        album = Album.objects.get(id=1)
        self.assertEqual(album.title, 'Djangle Today')
        \"""
        
        pass

""")

test_case_import_template = Template("""from .{{ model.lower() }} import {{ model.capitalize() }}TestCase""")
