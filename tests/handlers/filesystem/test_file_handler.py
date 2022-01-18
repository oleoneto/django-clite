import os
import unittest
from pathlib import Path
from tests import CliTestCase
from click.testing import CliRunner
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.template_handler import TemplateHandler
from cli.handlers.filesystem.directory import Directory
from cli.handlers.filesystem.template import Template

runner = CliRunner()


class FileHandlerTestCase(CliTestCase):
    # Necessary files
    files = [
        'example1.rb',
        'example2.rb',
        'example3.rb',
        'example4.rb',
        'example5.rb',
        'example6.rb',
    ]

    def setUp(self) -> None:
        super(FileHandlerTestCase, self).setUp()

        [Path(file).touch() for file in self.files]

    def tearDown(self) -> None:
        super(FileHandlerTestCase, self).tearDown()

        [Path(file).unlink() for file in self.files]

    def test_dry_create_file(self):
        with self.runner.isolated_filesystem(self._tests_directory):
            handler = FileHandler(dry=True)
            result = handler.create_file(content='# an example file', filename='example.test.py', path='./dummy')
            self.assertEqual(result.code, 'create_skipped')
            self.assertEqual(result.description, 'File was not created. Skipped with DRY flag.')

    def test_create_file(self):
        with self.runner.isolated_filesystem():
            handler = FileHandler(force=True)
            result = handler.create_file(content='# an example file', filename='example.test.py', path='./dummy')
            self.assertEqual(result.code, 'created')
            self.assertEqual(result.description, 'File was created successfully.')

    # @unittest.skip('Reimplementing')
    def test_skip_creation_of_existing_file(self):
        with self.runner.isolated_filesystem():
            handler = FileHandler(force=True)
            result = handler.create_file(content='# an example file', filename='example_2.test.py', path='./dummy')
            self.assertEqual(result.code, 'created')
            self.assertEqual(result.description, 'File was created successfully.')

            handler = FileHandler(force=False)
            result = handler.create_file(content='# an example file', filename='example_2.test.py', path='./dummy')
            self.assertEqual(result.code, 'not_created')
            self.assertEqual(result.description, 'File was not created. File already exists.')

    @unittest.skip('Reimplementing')
    def test_dry_destroy_file(self):
        with runner.isolated_filesystem():
            handler = FileHandler(dry=True)
            result = handler.remove_file(filename='example.test.py', path='./dummy')
            self.assertEqual(result.code, 'delete_skipped')
            self.assertEqual(result.description, 'File was not deleted. Skipped with DRY flag.')

    @unittest.skip('Reimplementing')
    def test_skip_destruction_of_non_existing_file(self):
        with runner.isolated_filesystem():
            handler = FileHandler()
            result = handler.remove_file(filename='nonexistent.test.py', path='./dummy')
            self.assertEqual(result.code, 'not_deleted')
            self.assertEqual(result.description, 'File was not deleted. File does not exist.')

    # FIXME: Need to destroy file in isolated filesystem
    # Current error state: File does not exist.
    @unittest.skip('Reimplementing')
    def test_destroy_file(self):
        with runner.isolated_filesystem():
            create_handler = FileHandler(force=True, dry=False, verbose=True)
            delete_handler = FileHandler()

            created = create_handler.create_file(filename='delete.test.py', content='# example file', path='.')

            deleted = delete_handler.remove_file(filename='delete.test.py', path='.')

            self.assertEqual(created.code, 'created')
            self.assertEqual(deleted.code, 'deleted')
            self.assertEqual(deleted.description, 'File was deleted successfully.')

    @unittest.skip('Reimplementing')
    def test_create_directory(self):
        handler = FileHandler()

        files = [Template('app.py', '# {{ name }} = lambda x: x*x', raw=True)]
        folder = Directory('models', [Directory('signals')], files)
        template_handler = TemplateHandler(scope='project')

        with runner.isolated_filesystem():
            result = handler.create_folder(folder, template_handler)

        self.assertEqual(True, result)

    @unittest.skip('Reimplementing')
    def test_append_to_file(self):
        with runner.isolated_filesystem():
            handler = FileHandler()
            result = handler.append_to_file(content='# appended content', filename='example.test.py', path='./dummy')
            self.assertEqual(result.code, 'appended')
            self.assertEqual('Content was appended successfully.', result.description)

    @unittest.skip('Reimplementing')
    def test_find_file_for_existing_file(self):
        handler = FileHandler()
        result = handler.find_file(path='./dummy', filename='example.test.py')
        self.assertEqual('./dummy/example.test.py', result)

    @unittest.skip('Reimplementing')
    def test_find_file_for_non_existing_file(self):
        handler = FileHandler()
        result = handler.find_file(path='./dummy', filename='non_existing.test.py')
        self.assertIs(None, result)

    # TODO: Need to test Click file creation in isolated filesystems
    @unittest.skip('Reimplementing')
    def test_find_files_for_existing_files(self):
        handler = FileHandler()
        result = handler.find_files(path='./dummy', patterns=['example.test.py', 'example.test.rb'])

        self.assertEqual(2, len(result))

        for name, path in result.items():
            self.assertEqual(name, path.name)

    # TODO: Need to test Click file creation in isolated filesystems
    @unittest.skip('Reimplementing')
    def test_find_files_for_non_existing_files(self):
        handler = FileHandler()
        result = handler.find_files(path='./dummy', patterns=['non_existing.test.py', 'non_existing.test.rb'])
        self.assertEqual(0, len(result))
        self.assertDictEqual({}, result)


if __name__ == '__main__':
    unittest.main()
