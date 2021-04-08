from click.testing import CliRunner
from cli.commands.create import main as create


def test_project():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(create.project, ['website'])

    assert result.exit_code == 0
