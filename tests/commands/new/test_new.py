import os
import unittest
from pathlib import Path
from click.testing import CliRunner
from geny.core.filesystem.files import File
from geny.core.filesystem.directories import Directory
from django_clite.commands.new.main import new
from tests import parser as _  # noqa: F401


runner = CliRunner()


class CreatorTestCase(unittest.TestCase):
    def test_new_project(self):
        with runner.isolated_filesystem():
            command = "project"
            proj_name = "store"
            res = runner.invoke(new, [command, proj_name])  # noqa

            self.assertEqual(0, res.exit_code)
            self.assertEqual(b"", res.stdout_bytes)

            proj_dir = Path(proj_name)
            self.assertTrue(proj_dir.exists())
            self.assertTrue(proj_dir.is_dir())

            with open(Path(proj_dir) / "README.md") as f:
                line = f.readline()
                self.assertEqual("# store\n", line)

    def test_new_app(self):
        with runner.isolated_filesystem():
            cmd = "apps"
            app_name = "blogger"

            res = runner.invoke(new, [cmd, app_name])  # noqa
            self.assertEqual(0, res.exit_code)
            self.assertEqual(b"", res.stdout_bytes)

            app_dir = Path(app_name)
            self.assertTrue(app_dir.exists())
            self.assertTrue(app_dir.is_dir())

            self.assertEqual(
                [
                    "__init__.py",
                    "admin",
                    "apps.py",
                    "fixtures",
                    "forms",
                    "middleware",
                    "migrations",
                    "models",
                    "router",
                    "serializers",
                    "tasks",
                    "templates",
                    "templatetags",
                    "tests",
                    "urls.py",
                    "views",
                    "viewsets",
                ],
                sorted(os.listdir(app_name)),
            )
