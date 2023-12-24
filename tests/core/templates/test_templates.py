import unittest
from pathlib import Path
from cli.core.templates.template import TemplateParser


class TemplatesTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = TemplateParser(
            templates_dir=Path(""),
            context={},
        )

    def test_parse_string(self):
        template1 = """My name is {{ name }}"""
        output = self.parser.parse_string(template1, {'name': 'Leo'})
        self.assertEqual(output, "My name is Leo")

        template2 = """My name is {% if name %}{{ name.upper() }}{% else %}Unknown{% endif %}."""
        output = self.parser.parse_string(template2, {'name': 'leo'})
        self.assertEqual(output, 'My name is LEO.')

        output = self.parser.parse_string(template2, variables={})
        self.assertEqual(output, 'My name is Unknown.')
