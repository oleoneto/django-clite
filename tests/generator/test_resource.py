from click.testing import CliRunner
from django_clite.commands.generator import resource


def test_generate_resource():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(resource, ['test_admin'])

    assert result.exit_code == 0
    assert result.output == '1'
