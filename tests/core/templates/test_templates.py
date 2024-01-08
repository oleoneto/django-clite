import unittest
from tests import parser


class TemplatesTestCase(unittest.TestCase):
    def test_parse_string(self):
        template1 = """My name is {{ name }}"""
        output = parser.parse_string(template1, {"name": "Leo"})
        self.assertEqual(output, "My name is Leo")

        template2 = """My name is {% if name %}{{ name.upper() }}{% else %}Unknown{% endif %}."""
        output = parser.parse_string(template2, {"name": "leo"})
        self.assertEqual(output, "My name is LEO.")

        output = parser.parse_string(template2, variables={})
        self.assertEqual(output, "My name is Unknown.")
