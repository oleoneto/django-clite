from click.testing import CliRunner
from cli.commands.create import main as create
import unittest


class CreateTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_project(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(create.project, ['website'])

        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
