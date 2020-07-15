from click.testing import CliRunner
from cli.commands.generate import model


def test_generate_model():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(model, ['test_model'])

    assert result.exit_code == 0
    assert result.output == '1'
