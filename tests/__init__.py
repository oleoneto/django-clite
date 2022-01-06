# tests
import os
import shutil
import unittest
from click.testing import CliRunner


class CliTestCase(unittest.TestCase):
    _tests_directory = '/tmp/django-clite/tests'
    runner = CliRunner()

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.makedirs(cls._tests_directory)
        except FileExistsError or OSError:
            shutil.rmtree(cls._tests_directory)
            os.makedirs(cls._tests_directory)

        os.chdir(cls._tests_directory)

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.removedirs(cls._tests_directory)
        except FileNotFoundError:
            pass
        except OSError:
            shutil.rmtree(cls._tests_directory)

    def tearDown(self) -> None:
        self.runner = CliRunner()
