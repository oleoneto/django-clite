import unittest
from pathlib import Path
from click.testing import CliRunner
from geny.core.filesystem.files import File
from geny.core.filesystem.directories import Directory
from django_clite.commands.new.main import new
from tests import parser as _ # noqa: F401


runner = CliRunner()


class CreatorTestCase(unittest.TestCase):
    def test_new_directory(self):
        with runner.isolated_filesystem():
            name = "store"
            context = {"project": "store", "author": "Leo Neto"}

            inner_proj = Directory(name)

            proj = Directory(
                name=name,
                children=[
                    inner_proj,
                    Directory(name="staticfiles"),
                    Directory(
                        name="templates",
                        children=[
                            File(name="404.html", template="# {{ project }}"),
                            File(name="500.html", template="# {{ project }}"),
                        ],
                    ),
                    File(name="README.md", template="{{project}}/readme.tpl"), # TODO: switch to template file
                    File(name="a.py", template="# {{ project }}"),
                    File(name="b.py", content="# content"),
                ],
            )

            proj.create(**context)

            self.assertTrue(proj.path().exists())
            self.assertTrue(proj.path().is_dir())
            self.assertEqual(3, len(proj.dirs))
            self.assertEqual(3, len(proj.files))

            # Template file:
            self.assertEqual("store/readme.tpl\n", proj.files[0].path(proj.path()).read_text())

            # Template literal
            self.assertEqual("# store\n", proj.files[1].path(proj.path()).read_text())

            # Content literal
            self.assertEqual("# content\n", proj.files[2].path(proj.path()).read_text())

    def test_new_project(self):
        with runner.isolated_filesystem():
            command = "project"
            proj_name = "store"
            res = runner.invoke(new, [command, proj_name]) # noqa

            self.assertEqual(0, res.exit_code)
            self.assertEqual(b'', res.stdout_bytes)

            proj_dir = Path(proj_name)
            self.assertTrue(proj_dir.exists())
            self.assertTrue(proj_dir.is_dir())

            with open(Path(proj_dir) / "README.md") as f:
                line = f.readline()
                self.assertEqual("# store\n", line)

    def test_new_app(self):
        pass # TODO: Implement test_new_app
