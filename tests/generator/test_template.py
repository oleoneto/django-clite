from click.testing import CliRunner
from django_clite.commands.generator import template


def test_generate_template():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(template, ['test_template'])

    assert result.exit_code == 0
    assert result.output == '1'
