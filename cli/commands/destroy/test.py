import click
import inflection
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


SUPPORTED_SCOPES = ['model', 'viewset']


@click.command()
@click.argument('name', required=True)
@click.option('-s', '--scope', type=click.Choice(SUPPORTED_SCOPES), required=True)
@click.option('--full', is_flag=True, help=f'Destroy all tests for {SUPPORTED_SCOPES}')
@click.pass_context
def test(ctx, name, scope, full):
    """
    Destroys TestCases.
    """

    def destroy(n, s):
        resource_destroyer(
            n,
            parent='tests',
            package=inflection.pluralize(s),
            scope='TestCase',
            **ctx.obj
        )

    if full:
        [destroy(name, s) for s in SUPPORTED_SCOPES]
    else:
        destroy(name, scope)
