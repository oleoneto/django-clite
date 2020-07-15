from click.testing import CliRunner
from cli.commands.generate import view


def test_generate_view():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(view, ['test_view'])

    assert result.exit_code == 0
    assert result.output == '1'
