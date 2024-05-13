import os
import unittest
import pathlib

from click.testing import CliRunner
from django.core.management import call_command
from django.core.management.commands import startapp

from geny.core.filesystem.filesystem import working_directory
from django_clite.commands.generate.main import generate
from django_clite.commands.destroy.main import destroy

runner = CliRunner()


class DestroyerTestCase(unittest.TestCase):
    # App-level resources

    def test_destroy_admin(self):
        with runner.isolated_filesystem():
            app = "blog"
            call_command(startapp.Command(), app, verbosity=0)

            with working_directory(app):
                _ = runner.invoke(generate, ["admin", "article"])  # noqa
                res = runner.invoke(destroy, ["admin", "article"])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn("admin", os.listdir())
                self.assertNotIn("article.py", os.listdir("admin"))

                # Inspect imports
                with open(pathlib.Path("admin") / '__init__.py', 'r') as f:
                    self.assertEqual('', f.read())

    def test_destroy_admin_inline(self):
        with runner.isolated_filesystem():
            app = "blog"
            call_command(startapp.Command(), app, verbosity=0)

            with working_directory(app):
                _ = runner.invoke(generate, ["admin-inline", "article"])  # noqa
                res = runner.invoke(destroy, ["admin-inline", "article"])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn("admin", os.listdir())
                self.assertIn("inlines", os.listdir("admin"))
                self.assertNotIn("article.py", os.listdir("admin/inlines"))

                # Inspect imports
                with open(pathlib.Path('admin/inlines') / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import ArticleInline', f.read())

    def test_destroy_fixture(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "fixture"
                resource_dir = "fixtures"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("article.json", os.listdir(resource_dir))

    def test_destroy_form(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "form"
                resource_dir = "forms"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("article.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import ArticleForm', f.read())

    def test_destroy_manager(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "manager"
                resource_dir = "managers"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertNotIn("article.py", os.listdir(f"models/{resource_dir}"))

                # Inspect imports
                with open(pathlib.Path(f"models/{resource_dir}") / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import ArticleManager', f.read())

    def test_destroy_model(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "model"
                resource_dir = "models"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertIn("__init__.py", os.listdir(resource_dir))
                self.assertNotIn("article.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import Article', f.read())

    def test_destroy_serializer(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "serializer"
                resource_dir = "serializers"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("article.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import Article', f.read())

    def test_destroy_signal(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article_created"
                command = "signal"
                resource_dir = "signals"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertNotIn(
                    "article_created.py", os.listdir(f"models/{resource_dir}")
                )

                # Inspect imports
                with open(pathlib.Path(f"models/{resource_dir}") / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article_created import article_created', f.read())

    def test_destroy_tag(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "now"
                command = "tag"
                resource_dir = "templatetags"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("now.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .now import now', f.read())

    def test_destroy_templates(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "template"
                resource_dir = "templates"

                _ = runner.invoke(generate, [command, resource, "--full"])  # noqa
                res = runner.invoke(destroy, [command, resource, "--full"])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotEqual(
                    [
                        "article_create.html",
                        "article_detail.html",
                        "article_list.html",
                        "article_update.html",
                    ],
                    sorted(os.listdir(resource_dir)),
                )

    def test_destroy_model_tests(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "test"
                resource_dir = "models"

                _ = runner.invoke(generate, [command, resource, "--scope", "model"])  # noqa
                res = runner.invoke(destroy, [command, resource, "--scope", "model"])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("tests"))
                self.assertNotIn("article_test.py", os.listdir(f"tests/{resource_dir}"))

                # Inspect imports
                with open(pathlib.Path(f"tests/{resource_dir}") / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article_test import ArticleTestCase', f.read())

    def test_destroy_viewset_tests(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "test"
                resource_dir = "viewsets"

                _ = runner.invoke(generate, [command, resource, "--scope", "viewset"])  # noqa
                res = runner.invoke(destroy, [command, resource, "--scope", "viewset"])  # noqa

                print(res.return_value)
                print(res.output)

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("tests"))
                self.assertNotIn("article_test.py", os.listdir(f"tests/{resource_dir}"))

                # Inspect imports
                with open(pathlib.Path(f"tests/{resource_dir}") / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article_test import ArticleTestCase', f.read())

    def test_destroy_validator(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "phone_number"
                command = "validator"
                resource_dir = "validators"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir("models"))
                self.assertNotIn("phone_number.py", os.listdir(f"models/{resource_dir}"))

                # Inspect imports
                with open(pathlib.Path(f"models/{resource_dir}") / '__init__.py', 'r') as f:
                    self.assertNotIn('from .phone_number import phone_number', f.read())

    def test_destroy_views(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "homepage"
                command = "view"
                resource_dir = "views"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("homepage.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .homepage import homepage', f.read())

    def test_destroy_viewset(self):
        with runner.isolated_filesystem():
            app_dir = "blog"
            call_command(startapp.Command(), app_dir, verbosity=0)

            with working_directory(app_dir):
                resource = "article"
                command = "viewset"
                resource_dir = "viewsets"

                _ = runner.invoke(generate, [command, resource])  # noqa
                res = runner.invoke(destroy, [command, resource])  # noqa

                self.assertEqual(0, res.exit_code)
                self.assertIn(resource_dir, os.listdir())
                self.assertNotIn("article.py", os.listdir(resource_dir))

                # Inspect imports
                with open(pathlib.Path(resource_dir) / '__init__.py', 'r') as f:
                    self.assertNotIn('from .article import ArticleViewSet', f.read())
