import unittest
from pathlib import Path
from click.testing import CliRunner

from cli.core.filesystem.transformations import (
    DeleteFile,
    MoveFile,
    AddLineToFile,
    RemoveLineFromFile
)

runner = CliRunner()


class TransformationsTestCase(unittest.TestCase):
    def test_add_line(self):
        file = Path("new.scratch")

        with runner.isolated_filesystem():
            file.write_text("line_1\n")

            AddLineToFile(file, "line_2").run()
            self.assertEqual("line_1\nline_2\n", file.read_text('utf-8'))

            AddLineToFile(file, "line_3").run()
            self.assertEqual("line_1\nline_2\nline_3\n", file.read_text('utf-8'))

    def test_remove_line(self):
        file = Path("new.scratch")

        with runner.isolated_filesystem():
            file.write_text("line_1\nline_2\n")

            # Do nothing
            RemoveLineFromFile(file, "line_3").run()
            self.assertEqual("line_1\nline_2\n", file.read_text('utf-8'))

            # Pop string
            RemoveLineFromFile(file, "line_1").run()
            self.assertEqual("line_2\n", file.read_text('utf-8'))

    def test_move_file(self):
        source = "file.py"
        target = "new.py"

        with runner.isolated_filesystem():
            Path(source).touch()
            Path(target).touch()

            self.assertTrue(Path(source).exists())
            self.assertTrue(Path(target).exists())

            MoveFile(source, target).run()

            self.assertFalse(Path(source).exists())
            self.assertTrue(Path(target).exists())

    def test_delete_file(self):
        source = "file.py"
        file = Path(source)

        with runner.isolated_filesystem():
            file.touch()
            self.assertTrue(file.exists())

            DeleteFile(source).run()

            self.assertFalse(file.exists())
