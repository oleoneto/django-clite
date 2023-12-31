import unittest
from django.core.management import call_command
from django.core.management.commands import startproject, startapp
from click.testing import CliRunner

from cli.core.filesystem.filesystem import working_directory
from cli.core.filesystem.finder import core_project_files, project_and_app_names

runner = CliRunner()


class FinderTestCase(unittest.TestCase):
    def test_find_core_project_files(self):
        with runner.isolated_filesystem():
            location = "project"

            cmd = startproject.Command()
            call_command(cmd, location, verbosity=0)

            files = core_project_files(location)
            self.assertEqual({"manage.py"}, files.keys())

            with working_directory(location):
                files = core_project_files(location)
                self.assertEqual({"wsgi.py", "asgi.py"}, files.keys())

    def test_project_and_app_name(self):
        with runner.isolated_filesystem():
            project = "website"
            app1 = "blog"
            app2 = "store"

            # Project
            cmd = startproject.Command()
            call_command(cmd, project, verbosity=0)

            # Apps
            with working_directory(project):
                cmd = startapp.Command()
                call_command(cmd, app1)
                call_command(cmd, app2)

                files1 = core_project_files(app1)
                files2 = core_project_files(app2)

            project_name1, app_name1 = project_and_app_names(files1)
            project_name2, app_name2 = project_and_app_names(files2)

            self.assertEqual("website", project_name1)
            self.assertEqual("website", project_name2)

            self.assertEqual("blog", app_name1)
            self.assertEqual("store", app_name2)
