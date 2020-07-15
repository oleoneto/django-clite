from click.testing import CliRunner
from cli.commands.generate import admin


def test_generate_admin():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(admin, ['test_admin'])

    assert result.exit_code == 0
