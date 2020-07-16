from click.testing import CliRunner
from cli.commands.run.main import create_compose


def test_create_settings():
    runner = CliRunner()
    result = runner.invoke(create_compose)
    assert result.exit_code == 0
