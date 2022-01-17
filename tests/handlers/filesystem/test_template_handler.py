import unittest
from cli.handlers.filesystem.template_handler import TemplateHandler


class TemplateHandlerTestCase(unittest.TestCase):
    def test_parse_template_file(self):
        handler = TemplateHandler()
        template = 'example.tpl'
        parsed_template = handler.parsed_template(template, context={'name': 'Leo'})
        self.assertEqual(parsed_template, 'Hello, Leo!')

    def test_parse_template_file_under_a_directory(self):
        handler = TemplateHandler(scope='shared')
        template = 'example.tpl'
        parsed_template = handler.parsed_template(template, context={'path': 'cli/templates/shared/'})
        self.assertEqual(parsed_template, 'Shared template at: cli/templates/shared/')

    def test_parse_template_string(self):
        handler = TemplateHandler()
        template1 = """Hello, {{ name }}!"""
        template2 = """Hello, person!"""
        parsed_template1 = handler.parsed_template(template1, context={'name': 'Leo'}, raw=True)
        parsed_template2 = handler.parsed_template(template2, raw=True)
        self.assertEqual(parsed_template1, 'Hello, Leo!')
        self.assertEqual(parsed_template2, 'Hello, person!')

    def test_do_not_parse_non_existing_template_file(self):
        handler = TemplateHandler()
        template = "nonexistent.rb"
        result = handler.parsed_template(template, context={'name': 'Leo'})
        self.assertRaises(FileNotFoundError)
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
