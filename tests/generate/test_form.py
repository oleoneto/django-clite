from click.testing import CliRunner
from cli.commands.generate import form


def test_generate_form():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(form, ['test_form'])

    assert result.exit_code == 0
    assert result.output == '1'
