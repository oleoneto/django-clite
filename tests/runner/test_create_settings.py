from click.testing import CliRunner
from django_clite.commands.runner.main import create_settings


def test_create_settings():
    runner = CliRunner()
    result = runner.invoke(create_settings)
    assert result.exit_code == 0
