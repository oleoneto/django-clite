from click.testing import CliRunner
from django_clite.commands.generator import serializer


def test_generate_serializer():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(serializer, ['test_serializer'])

    assert result.exit_code == 0
    assert result.output == '1'
