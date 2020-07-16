import pytest
from click.testing import CliRunner


@pytest.fixture(scope='function')
def run(request):
    return CliRunner()
