from click.testing import CliRunner
from cli.commands.generate import viewset


def test_generate_viewset():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(viewset, ['test_viewset'])

    assert result.exit_code == 0
    assert result.output == '1'
