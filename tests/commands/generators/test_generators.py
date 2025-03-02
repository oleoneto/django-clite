import os
import pathlib
import unittest

from click.testing import CliRunner
from django.core.management import call_command
from django.core.management.commands import startapp, startproject

from geny.core.filesystem.filesystem import working_directory
from django_clite.commands.generate.main import generate
from django_clite.commands.destroy.main import destroy

from tests import temp_dir


runner = CliRunner()

app_name = "blogger"


class GeneratorTestCase(unittest.TestCase):
    def setUp(self):
        # Generates a base app wherein all generators should create their modules
        with working_directory(temp_dir):
            call_command(startapp.Command(), app_name, verbosity=0)

    def tearDown(self):
        # Removes files created in setUp()
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            root_path = pathlib.Path(root)
            for name in files:
                if name == ".keep":
                    continue
                (root_path / name).unlink()
            for name in dirs:
                (root_path / name).rmdir()

    def test_require_app_scope_to_run_generators(self):
        with working_directory(temp_dir):
            commands = [
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
            ]

            for command in commands:
                with self.subTest(cmd="generate"):
                    res = runner.invoke(generate, [command, "article"])  # noqa
                    self.assertNotEqual(0, res.exit_code)
                    self.assertIn("app was not detected", res.output)

                with self.subTest(cmd="destroy"):
                    res = runner.invoke(destroy, [command, "article"])  # noqa
                    self.assertNotEqual(0, res.exit_code)
                    self.assertIn("app was not detected", res.output)

    def test_require_project_scope_to_generate_dockerfile(self):
        cmd = "dockerfile"

        # Failure

        with self.subTest(name="random directory"):
            with working_directory(temp_dir):
                res = runner.invoke(generate, [cmd])  # noqa
                self.assertNotEqual(0, res.exit_code)
                self.assertIn("project was not detected", res.output)

        with self.subTest(name="app directory"):
            with working_directory(temp_dir / app_name):
                res = runner.invoke(generate, [cmd])  # noqa
                self.assertNotEqual(0, res.exit_code)
                self.assertIn("project was not detected", res.output)

        # Success

        with runner.isolated_filesystem():
            project = "project"
            call_command(startproject.Command(), project, verbosity=0)

            with working_directory(project):
                with self.subTest(name="no flags"):
                        res = runner.invoke(generate, [cmd])  # noqa
                        self.assertEqual(0, res.exit_code)
                        self.assertIn("Dockerfile", os.listdir())

                        # Destroy files
                        d_res = runner.invoke(destroy, [cmd])  # noqa
                        self.assertEqual(0, d_res.exit_code)
                        self.assertNotIn("Dockerfile", os.listdir())

                with self.subTest(name="with flags"):
                    res = runner.invoke(generate, [cmd, "--compose"])  # noqa
                    self.assertEqual(0, res.exit_code)
                    self.assertIn("Dockerfile", os.listdir())
                    self.assertIn("docker-compose.yaml", os.listdir())

                    # Destroy file
                    d_res = runner.invoke(destroy, [cmd, "--compose"])  # noqa

                    self.assertEqual(0, d_res.exit_code)
                    self.assertNotIn("Dockerfile", os.listdir())
                    self.assertNotIn("docker-compose.yaml", os.listdir())

    def test_generate_app_modules(self):
        generators = {
            "admin": "admin",
            "form": "forms",
            "model": "models",
            "serializer": "serializers",
            "viewset": "viewsets",
            "view": "views",
            "tag": "templatetags",
        }

        import_pattern = "from .article import [Aa]rticle([a-zA-Z]+)?$"

        for scope, package in generators.items():
            with self.subTest(scope=scope):
                with working_directory(temp_dir / app_name):
                    g_res = runner.invoke(generate, [scope, "article"])  # noqa

                    self.assertEqual(0, g_res.exit_code)
                    self.assertIn(package, os.listdir())
                    self.assertIn("article.py", os.listdir(package))

                    # Inspect imports
                    with open(pathlib.Path(package) / "__init__.py", "r") as f:
                        self.assertRegex(f.read(), import_pattern)

                    # Destroy file
                    d_res = runner.invoke(destroy, [scope, "article"])  # noqa

                    self.assertEqual(0, d_res.exit_code)
                    self.assertIn(package, os.listdir())
                    self.assertNotIn("article.py", os.listdir(package))

                    # Inspect imports
                    with open(pathlib.Path(package) / "__init__.py", "r") as f:
                        self.assertEqual(f.read(), "")

    def test_generate_model_scoped_app_modules(self):
        generators = {
            "manager":   "managers",
            "signal":    "signals",
            "validator": "validators",
        }

        for scope, package in generators.items():
            with self.subTest(scope=scope):
                with working_directory(temp_dir / app_name):
                    g_res = runner.invoke(generate, [scope, "article"])  # noqa

                    self.assertEqual(0, g_res.exit_code)
                    self.assertIn(package, os.listdir("models"))
                    self.assertIn("article.py", os.listdir(f"models/{package}"))

                    # Inspect imports
                    with open(pathlib.Path(f"models/{package}") / "__init__.py", "r") as f:
                        self.assertRegex(f.read(), 'from .article import [Aa]rticle(_?[a-zA-Z]+)?$')

                    # Destroy file
                    d_res = runner.invoke(destroy, [scope, "article"])  # noqa

                    self.assertEqual(0, d_res.exit_code)
                    self.assertIn(package, os.listdir("models"))
                    self.assertNotIn("article.py", os.listdir(f"models/{package}"))

                    # Inspect imports
                    with open(pathlib.Path(f"models/{package}") / "__init__.py", "r") as f:
                        self.assertEqual(f.read(), "")

    def test_generate_tests(self):
        generators = {
            "model": "models",
            "viewset": "viewsets",
        }

        for scope, package in generators.items():
            with self.subTest(scope=scope):
                with working_directory(temp_dir / app_name):
                    g_res = runner.invoke(generate, ["test", "article", "--scope", scope])  # noqa

                    self.assertEqual(0, g_res.exit_code)
                    self.assertIn(package, os.listdir("tests"))
                    self.assertIn("article_test.py", os.listdir(f"tests/{package}"))

                    # Inspect imports
                    with open(pathlib.Path(f"tests/{package}") / "__init__.py", "r") as f:
                        self.assertRegex(f.read(), 'from .article_test import ArticleTestCase$')

                    # Destroy file
                    d_res = runner.invoke(destroy, ["test", "article", "--scope", scope])  # noqa

                    self.assertEqual(0, d_res.exit_code)
                    self.assertIn(package, os.listdir("tests"))
                    self.assertNotIn("article_test.py", os.listdir(f"tests/{package}"))

                    # Inspect imports
                    with open(pathlib.Path(f"tests/{package}") / "__init__.py", "r") as f:
                        self.assertEqual(f.read(), "")

    def test_admin_inline(self):
        cmd = "admin-inline"

        with working_directory(temp_dir / app_name):
            g_res = runner.invoke(generate, [cmd, "article"])  # noqa

            self.assertEqual(0, g_res.exit_code)
            self.assertIn("admin", os.listdir())
            self.assertIn("inlines", os.listdir("admin"))
            self.assertIn("article.py", os.listdir("admin/inlines"))

            # Inspect imports
            with open(pathlib.Path("admin/inlines") / "__init__.py", "r") as f:
                self.assertRegex(f.read(), 'from .article import ArticleInline$')

            # Destroy file
            d_res = runner.invoke(destroy, [cmd, "article"])  # noqa

            self.assertEqual(0, d_res.exit_code)
            self.assertIn("admin", os.listdir())
            self.assertIn("inlines", os.listdir("admin"))
            self.assertNotIn("article.py", os.listdir("admin/inlines"))

            # Inspect imports
            with open(pathlib.Path("admin/inlines") / "__init__.py", "r") as f:
                self.assertEqual(f.read(), "")

    def test_fixture(self):
        cmd = "fixture"
        package = "fixtures"

        with working_directory(temp_dir / app_name):
            g_res = runner.invoke(generate, [cmd, "article"])  # noqa

            self.assertEqual(0, g_res.exit_code)
            self.assertIn(package, os.listdir())
            self.assertIn("article.json", os.listdir(package))

            # Destroy file
            d_res = runner.invoke(destroy, [cmd, "article"])  # noqa

            self.assertEqual(0, d_res.exit_code)
            self.assertIn(package, os.listdir())
            self.assertNotIn("article.json", os.listdir(package))

    def test_template(self):
        cmd = "template"
        dir_ = "templates"

        with working_directory(temp_dir / app_name):
            g_res = runner.invoke(generate, [cmd, "article", "--full"])  # noqa

            self.assertEqual(0, g_res.exit_code)
            self.assertIn(dir_, os.listdir())
            self.assertEqual(
                [
                    "article_create.html",
                    "article_detail.html",
                    "article_list.html",
                    "article_update.html",
                ],
                sorted(os.listdir(dir_)),
            )

            # Destroy file
            d_res = runner.invoke(destroy, [cmd, "article", "--full"])  # noqa

            self.assertEqual(0, d_res.exit_code)
            self.assertIn(dir_, os.listdir())
            self.assertNotEqual(
                [
                    "article_create.html",
                    "article_detail.html",
                    "article_list.html",
                    "article_update.html",
                ],
                sorted(os.listdir(dir_)),
            )
