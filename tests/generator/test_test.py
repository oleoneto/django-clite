from click.testing import CliRunner
from django_clite.commands.generator import test


def test_generate_test():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(test, ['test_test'])

    assert result.exit_code == 0
    assert result.output == '1'
