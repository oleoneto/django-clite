from click.testing import CliRunner
from django_clite.commands.generator import viewset


def test_generate_viewset():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(viewset, ['test_viewset'])

    assert result.exit_code == 0
    assert result.output == '1'
