import unittest
from click.testing import CliRunner

from cli.core.filesystem.files import File

runner = CliRunner()


class FileTestCase(unittest.TestCase):
    def test_create_file(self):
        with runner.isolated_filesystem():
            file = File(
                "new.scratch",
                content="{{greeting}} world!",
                context={"greeting": "Hello"},
            )
            file.create()

            self.assertTrue(file.path().exists())
            self.assertTrue(file.path().is_file())
            self.assertEqual("Hello world!", file.contents())

    def test_create_file_and_intermittent_directories(self):
        with runner.isolated_filesystem():
            file = File(
                "files/1/2/new.scratch",
                content="{{greeting}} world!",
                context={"greeting": "Hello"},
            )
            file.create()

            self.assertTrue(file.path().exists())
            self.assertTrue(file.path().is_file())
            self.assertEqual("Hello world!", file.contents())

    def test_delete_file(self):
        with runner.isolated_filesystem():
            file = File(
                "new.scratch",
                content="{{greeting}} world!",
                context={"greeting": "Hello"},
            )
            file.create()

            self.assertTrue(file.path().exists())

            file.destroy()

            self.assertFalse(file.path().exists())
