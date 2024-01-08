import os
import unittest
from click.testing import CliRunner
from django.core.management import call_command
from django.core.management.commands import startapp, startproject

from cli.core.filesystem.filesystem import working_directory
from cli.commands.generate.main import generate


runner = CliRunner()


class GeneratorTestCase(unittest.TestCase):
    def test_generators_require_app_dir(self):
        with runner.isolated_filesystem():
            commands = {
                "admin",
                "fixture",
                "form",
                "manager",
                "model",
                "scaffold",
                "serializer",
                "signal",
                "tag",
                "template",
                "validator",
                "view",
                "viewset",
            }

            for command in commands:
                res = runner.invoke(generate, [command, "article"])
                self.assertNotEqual(0, res.exit_code)
                self.assertIn("app was not detected", res.output)

    # App-level resources

    def test_generate_admin(self):
        with runner.isolated_filesystem():
            app = "blog"
            call_command(startapp.Command(), app, verbosity=0)

            with working_directory(app):
                res = runner.invoke(generate, ["admin", "article"])

                self.assertEqual(0, res.exit_code)
                self.assertIn("admin", os.listdir())
                self.assertIn("article.py", os.listdir("admin"))

    def test_generate_admin_inline(self):
        with runner.isolated_filesystem():
            app = "blog"
            call_command(startapp.Command(), app, verbosity=0)

            with working_directory(app):
                res = runner.invoke(generate, ["admin-inline", "article"])

                self.assertEqual(0, res.exit_code)
                self.assertIn("admin", os.listdir())
                self.assertIn("inlines", os.listdir("admin"))
                self.assertIn("article.py", os.listdir("admin/inlines"))

    def test_generate_fixture(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "fixture"
                resource_dir = "fixtures"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn(
                    "article.json", os.listdir(resource_dir)
                )  # FIX: fixture file should be plural

    def test_generate_form(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "form"
                resource_dir = "forms"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("article.py", os.listdir(resource_dir))

    def test_generate_manager(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "manager"
                resource_dir = "managers"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertIn("article.py", os.listdir(f"models/{resource_dir}"))

    def test_generate_model(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "model"
                resource_dir = "models"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("article.py", os.listdir(resource_dir))

    def test_generate_serializer(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "serializer"
                resource_dir = "serializers"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("article.py", os.listdir(resource_dir))

    def test_generate_signal(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article_created"
                command = "signal"
                resource_dir = "signals"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertIn(
                    "article_created.py", os.listdir(f"models/{resource_dir}")
                )

    def test_generate_tag(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "now"
                command = "tag"
                resource_dir = "templatetags"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("now.py", os.listdir(resource_dir))

    def test_generate_templates(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "template"
                resource_dir = "templates"

                res = runner.invoke(generate, [command, resource, "--full"])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertEqual(
                    [
                        "article_create.html",
                        "article_detail.html",
                        "article_list.html",
                        "article_update.html",
                    ],
                    sorted(os.listdir(resource_dir)),
                )

    def test_generate_tests(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "test"
                resource_dir = "models"

                res = runner.invoke(generate, [command, resource, "--scope", "model"])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("tests"))
                self.assertIn("article_test.py", os.listdir(f"tests/{resource_dir}"))

            with working_directory(app_dir):
                resource = "article"
                command = "test"
                resource_dir = "viewsets"

                res = runner.invoke(generate, [command, resource, "--scope", "viewset"])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("tests"))
                self.assertIn("article_test.py", os.listdir(f"tests/{resource_dir}"))

    def test_generate_validator(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "phone_number"
                command = "validator"
                resource_dir = "validators"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertIn("phone_number.py", os.listdir(f"models/{resource_dir}"))

    def test_generate_views(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "view"
                resource_dir = "views"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("article.py", os.listdir(resource_dir))

    def test_generate_viewset(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "viewset"
                resource_dir = "viewsets"

                res = runner.invoke(generate, [command, resource])

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("article.py", os.listdir(resource_dir))

    # Project-level resource

    def test_generate_dockerfile_requires_project_dir(self):
        res = runner.invoke(generate, ["dockerfile"])
        self.assertNotEqual(0, res.exit_code)
        self.assertIn("project was not detected", res.output)

    def test_generate_dockerfile_requires_non_app_dir(self):
        with runner.isolated_filesystem():
            app = "app"
            call_command(startapp.Command(), app, verbosity=0)

            with working_directory(app):
                res = runner.invoke(generate, ["dockerfile"])
                self.assertNotEqual(0, res.exit_code)
                self.assertIn("project was not detected", res.output)

    def test_generate_dockerfile(self):
        with runner.isolated_filesystem():
            project = "project"
            call_command(startproject.Command(), project, verbosity=0)

            with working_directory(project):
                res = runner.invoke(generate, ["dockerfile"])

                self.assertEqual(0, res.exit_code)
                self.assertIn("Dockerfile", os.listdir())

        with runner.isolated_filesystem():
            project = "project"
            call_command(startproject.Command(), project, verbosity=0)

            with working_directory(project):
                res = runner.invoke(generate, ["dockerfile", "--docker-compose"])

                self.assertEqual(0, res.exit_code)
                self.assertIn("Dockerfile", os.listdir())
                self.assertIn("docker-compose.yaml", os.listdir())
