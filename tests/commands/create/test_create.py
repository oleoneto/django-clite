import unittest
from click.testing import CliRunner
from cli.commands.create.main import create_project, create_applications
from tests import CliTestCase

runner = CliRunner()


class CreateCommandTestCase(CliTestCase):
    @unittest.skip('Not fully implemented')
    def test_create_project(self):
        with runner.isolated_filesystem():
            result = runner.invoke(create_project, ['website'])

            self.assertEqual(0, result.exit_code)
            # self.assertEqual(None, result.return_value)

    @unittest.skip('Not fully implemented')
    def test_do_not_create_project_with_duplicate_name(self):
        with runner.isolated_filesystem():
            result = runner.invoke(create_project, name='website')

        self.assertEqual(0, result.exit_code)
        self.assertEqual(0, result.return_value)

    @unittest.skip('Not fully implemented')
    def test_create_app(self):
        with runner.isolated_filesystem():
            result = runner.invoke(create_applications, apps=['blog'])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(0, result.return_value)

    @unittest.skip('Not fully implemented')
    def test_do_not_create_app_outside_a_project(self):
        with runner.isolated_filesystem():
            result = runner.invoke(create_applications, apps=['blog'])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(0, result.return_value)


if __name__ == '__main__':
    unittest.main()
