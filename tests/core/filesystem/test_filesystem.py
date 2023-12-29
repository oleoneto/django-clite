import os
import unittest
from click.testing import CliRunner

from cli.core.filesystem.filesystem import working_directory


runner = CliRunner()


class FileSystemTestCase(unittest.TestCase):
    def test_change_working_directory(self):
        with (runner.isolated_filesystem()):
            parent = "project"
            child1 = "project/child1"
            child2 = "project/child2"

            os.makedirs(child1)
            os.makedirs(child2)

            with working_directory(parent):
                self.assertTrue(os.getcwd().endswith(parent))

            with working_directory(child1):
                self.assertTrue(os.getcwd().endswith(child1))

            with working_directory(child2):
                self.assertTrue(os.getcwd().endswith(child2))
