from click.testing import CliRunner
from django_clite.commands.generator import form


def test_generate_form():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(form, ['test_form'])

    assert result.exit_code == 0
    assert result.output == '1'
